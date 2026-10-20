from scripts.audit_dataset import audit

def test_frozen_artifacts_independent_audit():
    report=audit()
    assert report['passed'], report['errors']
    assert report['records']==16606
