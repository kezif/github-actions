import pytest
import requests

SITE_URL = "https://url_short-1-a5698201.deta.app"
# SITE_URL = 'http://127.0.0.1:8000'
headers = {"Content-Type": "application/json", "accept": "application/json"}


def test_sanity():
    assert True


@pytest.mark.parametrize("link", ["github.com", "github"])
def test_unvalid_url(link):
    d = {"original_url": link}
    res = requests.post(SITE_URL, json=d, verify=False, headers=headers)
    assert res.status_code == 422, f"{link} invalid url test"


"""@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def test_valid_url(link):
    d = {'original_url': link}
    res = requests.post(SITE_URL, json=d, verify=False, headers=headers)

    assert int(res.status_code) == 200, f"Failed to shorten URL: {res.json()}"

    shorten_url = res.json().get("shorten_url")
    assert shorten_url is not None, f"Shortened URL not found in the response: {res.json()}"

"""


@pytest.mark.parametrize(
    "long_url",
    [
        "https://en.wikipedia.org/wiki/Atlantic_City%E2%80%93Brigantine_Connectori/Atlantic_City%E2%80%93Brigantine_Connectori/Atlantic_City%E2%80%93Brigantine_Connectori/Atlantic_City%E2%80%93Brigantine_Connectori/Atlantic_City%E2%80%93Brigantine_Connectori/Atlantic_City%E2%80%93Brigantine_Connectori/Atlantic_City%E2%80%93Brigantine_Connector"
    ],
)
def test_long_url(long_url):
    d = {"original_url": long_url}
    res = requests.post(SITE_URL, json=d, verify=False, headers=headers)
    assert int(res.status_code) == 200, f"Failed to shorten long URL: {res.json()}"


@pytest.mark.parametrize(
    "link",
    [
        "https://github.com/",
        "https://github.com/kezif/fabric",
        "https://www.linkedin.com/",
    ],
)
class TestShortening:
    mapping = {}  # hint that test suite use memory

    def test_valid_url_shorten(self, link):
        d = {"original_url": link}
        res = requests.post(SITE_URL, json=d, verify=False, headers=headers)

        assert res.status_code == 200, f"Failed to shorten URL: {res.json()}"

        shorten_url = res.json().get("shorten_url")
        self.mapping[link] = shorten_url
        assert (
            shorten_url is not None
        ), f"Shortened URL not found in the response: {res.json()}"

    def test_shorten_to_original_mapping(self, link):
        shorten_url_memory = self.mapping[link]
        res = requests.get(
            SITE_URL + f"/{shorten_url_memory}", verify=False, headers=headers
        )
        assert (
            link == res.json()["original_url"]
        ), f"shorten url doesnt correlate with original url {res.json()}  og:{link}"

    def test_short_info(self, link):
        shorten_url_memory = self.mapping[link]
        res = requests.get(
            SITE_URL + f"/info/{shorten_url_memory}", verify=False, headers=headers
        )
        jres = res.json()
        assert (
            jres["original_url"] is not None
        ), f"Original URL not found in the response: {res.json()}"
        assert (
            jres["shorten_url"] is not None
        ), f"Shorten URL not found in the response: {res.json()}"
        assert (
            jres["clicks"] is not None
        ), f"Cliks URL not found in the response: {res.json()}"
        assert (
            jres["created_at"] is not None
        ), f"Date of creation URL not found in the response: {res.json()}"

    @pytest.mark.skip(reason="database is readonly so no write functionality")
    def test_inc_number_of_cliks(self, link):
        shorten_url_memory = self.mapping[link]
        res = requests.get(
            SITE_URL + f"/{shorten_url_memory}", verify=False, headers=headers
        )
        og_click = int(res.json()["clicks"])
        res = requests.get(
            SITE_URL + f"/{shorten_url_memory}", verify=False, headers=headers
        )
        click2 = int(res.json()["clicks"])
        assert og_click + 1 == click2, "Number of cliks doesnt incriment"


# test_valid_url('https://github.com/')
