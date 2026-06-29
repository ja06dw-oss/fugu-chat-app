import os
from flask import Flask, request, render_template_string
from openai import OpenAI

API_KEY = "fish_722df7a206f76b067581c87a32a617b95fce3968ba6bddd2825e18bc9441d13f"  # ← 自分のキーに書き換え

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.sakana.ai/v1",
)

app = Flask(__name__)

# シンプルな HTML テンプレート（文字列で定義）
HTML = """
<!DOCTYPE html>
<html>
<head><title>Fugu Chat</title></head>
<body>
  <h1>Sakana Fugu チャット</h1>
  <form method="post">
    <label>モデル:</label>
    <select name="model">
      <option value="fugu">fugu</option>
      <option value="fugu-ultra">fugu-ultra</option>
    </select><br><br>
    <label>質問:</label><br>
    <textarea name="question" rows="4" cols="50"></textarea><br><br>
    <button type="submit">送信</button>
  </form>
  {% if answer %}
  <h2>回答:</h2>
  <pre>{{ answer }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    model = "fugu"
    if request.method == "POST":
        model = request.form.get("model", "fugu")
        question = request.form.get("question", "")
        if question:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": question}],
            )
            answer = response.choices[0].message.content
    return render_template_string(HTML, answer=answer, model=model)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)