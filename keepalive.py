"""
Streamlit Community CloudのアプリはHTTPアクセスだけでは起きないため、
実際にブラウザでページを開いて「Yes, get this app back up!」ボタンを
押しに行くスクリプト。

使い方:
1. 下の APP_URLS に、起こしたい自分のStreamlitアプリのURLを追加する
2. GitHub Actionsが自動でこのスクリプトを定期実行してくれる
"""

from playwright.sync_api import sync_playwright

# ここに自分のStreamlitアプリのURLを追加していく（増えたら行を足すだけ）
APP_URLS = [
    "https://risk-tolerance-diagnosis.streamlit.app",
    "https://rin-nisa-lifeplan-test.streamlit.app", 
]

WAKE_BUTTON_TEXTS = [
    "Yes, get this app back up!",
    "get this app back up",
]


def wake_app(playwright, url: str) -> None:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    print(f"[access] {url}")
    page.goto(url, timeout=30000, wait_until="domcontentloaded")

    # スリープ画面が出ていればボタンを探してクリックする
    woke = False
    for text in WAKE_BUTTON_TEXTS:
        try:
            button = page.get_by_text(text, exact=False)
            if button.count() > 0:
                button.first.click(timeout=5000)
                print(f"[wake] clicked wake button on {url}")
                woke = True
                # アプリが起動し切るまで少し待つ
                page.wait_for_timeout(15000)
                break
        except Exception:
            continue

    if not woke:
        print(f"[ok] {url} was already awake (or no button found)")

    browser.close()


def main() -> None:
    with sync_playwright() as playwright:
        for url in APP_URLS:
            try:
                wake_app(playwright, url)
            except Exception as e:
                print(f"[error] failed for {url}: {e}")


if __name__ == "__main__":
    main()
