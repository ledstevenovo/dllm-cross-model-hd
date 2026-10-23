# 事故：队列等待条件写错，导致 CUDA OOM

日期：2026-10-24 00:15。

## 发生了什么

我为两个 GPU 任务各写了一个"等当前采集结束再启动"的排队脚本，但**等待条件各不相同**：

```bash
# l256queue（正确）
while pgrep -f "collect_dream.py.*hotpotqa_eval800" >/dev/null; do sleep 60; done

# precqueue（错误）
while pgrep -f "collect_llada.py.*triviaqa_eval800" >/dev/null; do sleep 60; done
```

`precqueue` 等的是 **LLaDA TriviaQA** 的采集，而当时正在跑的是 **Dream HotpotQA** 的采集。
模式匹配不到任何进程 → **条件立即为假 → 精度对照采集立刻启动**。

## 后果

两个 8B 模型同时加载：

```
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 96.00 MiB.
GPU 0 has a total capacity of 31.48 GiB of which 56.38 MiB is free.
Process 173193 has 23.17 GiB memory in use.
```

- **Dream 的采集没有受影响**（它先拿到显存，继续跑到 463/800）；
- **精度对照采集直接崩溃**，未产生任何轨迹；
- 无数据损坏，无磁盘异常。

## 修复

抽出 `scripts/lib/gpu_wait.sh`，条件改为**两个独立判据**：

```bash
gpu_wait() {
  # 1) 任何 collector 进程在跑 -> 等
  pgrep -f "scripts/collect_(llada|dream)\.py" && sleep
  # 2) 显存占用 > 500 MiB -> 等（防止进程已退出但显存未释放）
  [ used -gt 500 ] && sleep
}
```

两个队列脚本都改用这个函数，不再依赖具体进程名。

## 教训

**"等待某个具体进程"是脆弱的排队方式。** 一旦模式写错，它不会报错，
而是**静默地立即放行**——这是最坏的失败模式（比报错更危险）。

正确做法是**等待资源本身可用**（显存低 + 无任何采集进程），
而不是等待"我以为会占用资源的那个进程"。

这与本项目之前那次"在运行中编辑 shell 脚本"的事故同型：
**都是用一个隐含假设（进程名匹配、bash 增量读取）替代显式检查**。

## 影响评估

| 项 | 影响 |
|---|---|
| Dream 含上下文 L64 采集 | ✅ 未受影响，继续 |
| 精度对照实验 | ⏳ 延后（已重新排队，现在正确等待） |
| L256 预测实验 | ⏳ 延后（同队列） |
| 已完成的分析与论文 | ✅ 无影响 |
