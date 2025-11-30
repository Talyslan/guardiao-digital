from src.infra.reputation.google_safebrowsing import GoogleSafeBrowsingService

def test_google_safe_dev_mode():
    svc = GoogleSafeBrowsingService()
    # sem chave, deve retornar safe (dev mode)
    res = svc.check_url("http://example.com")
    assert res.safe is True
