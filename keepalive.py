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

    # JSでの描画が終わるまでしっかり待つ
    page.goto(url, timeout=45000, wait_until="networkidle")
    # スリープ画面の描画が少し遅れることがあるので、念のため追加で待つ
    page.wait_for_timeout(5000)

    woke = False
    for text in WAKE_BUTTON_TEXTS:
        try:
            button = page.get_by_text(text, exact=False)
            button.wait_for(state="visible", timeout=8000)
            button.first.click(timeout=8000, force=True)
            print(f"[wake] clicked wake button on {url}")
            woke = True
            # アプリが起動し切るまでしっかり待つ
            page.wait_for_timeout(25000)
            break
        except Exception as e:
            print(f"[debug] button '{text}' not found or click failed: {e}")
            continue

    if not woke:
        print(f"[ok] {url} was already awake (no wake button found)")

    # 結果確認用に、最終的なページのタイトルを出力しておく
    try:
        print(f"[result] page title after visit: {page.title()}")
    except Exception:
        pass

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
  
