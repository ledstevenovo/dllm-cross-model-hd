"""Deterministic small models exercising the actual collector/sampler paths."""
from types import SimpleNamespace
import torch
from tests.fixtures.dream_generation_utils import DreamGenerationMixin
from transformers import PretrainedConfig

class PositionModel(torch.nn.Module):
    device=torch.device('cpu')
    def __init__(self):
        super().__init__()
        self.calls=0
        self.config=PretrainedConfig(mask_token_id=31,eos_token_id=2,pad_token_id=2,bos_token_id=1,vocab_size=32)
    def eval(self):return self
    def forward(self,x,*args,**kwargs):
        self.calls+=1
        logits=torch.zeros((*x.shape,32),device=x.device)
        for pos in range(x.shape[1]):logits[:,pos,3+pos%20]=4+pos*.05
        return SimpleNamespace(logits=logits)

class DreamPositionModel(PositionModel,DreamGenerationMixin):
    pass

class Tokenizer:
    eos_token_id=2
    def get_vocab(self):return {'<|endoftext|>':2,'<|eot_id|>':7,'<|im_end|>':7}
    def apply_chat_template(self,messages,**kwargs):
        if kwargs.get('tokenize',True) is False:return 'USER: '+messages[0]['content']+'\nASSISTANT:'
        return torch.tensor([[1,5,6]])
    def decode(self,ids,**kwargs):return ' '.join(map(str,ids))
    def batch_decode(self,rows,**kwargs):return [self.decode(r.tolist() if hasattr(r,'tolist') else r) for r in rows]
