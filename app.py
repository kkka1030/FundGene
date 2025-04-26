'''''''''
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from flask_cors import CORS  # 新增依赖

app = Flask(__name__)
CORS(app)  # 允许跨域（如果前后端分离）

# 设置 OpenAI API Key
client = OpenAI(
    api_key="sk-7k7v6qHOyaXe0kYwHKcwH4aUIhWokNRpTCL19CGmDbKWtBs7",  # 替换为你的 API Key
    base_url="https://api.zchat.tech/v1"
)

# 设定 AI 的角色
system_message = {
    "role": "system",
    "content": (
        "你是一位名叫FundGene的基金投资助手，用于给新人投资者提供投资基金的建议。"
        "你会根据用户的需求和风险承受能力，推荐适合的基金产品。"
        "如果对方问你一些与金融无关的奇怪的问题，你可以回答：“听不懂你在说什么哦，我只会投资基金呢”"
        
    )
}



# 记录对话历史
messages = [system_message]


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/strategy")
def strategy():
    return render_template("strategy.html")

# app.py

# 添加以下路由
@app.route("/behavior")
def behavior():
    return render_template("behavior.html")

@app.route("/risk")
def risk():
    return render_template("risk.html")

@app.route("/information")
def information():
    return render_template("information.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "输入内容不能为空"}), 400

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 也可以使用 "gpt-4"（如果你的 API 支持）
            messages=messages
        )

        ai_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_reply})

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
'''''''''''

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# AutoGen配置
config_list = config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["gpt-3.5-turbo"],
    },
)

# 初始化智能体
assistant = AssistantAgent(
    name="FundGene",
    system_message="""
    你是基金投资助手FundGene，专为新人投资者提供基金投资建议。
    根据用户需求和风险承受能力推荐合适基金产品。
    若遇到与金融无关的问题，回答：“听不懂你在说什么哦，我只会投资基金呢”
    若说一些与金融无关的事，你可以回答：“我是投资助手，别在这里发一些乱七八糟的无关的东西哦”
    """,
    llm_config={"config_list": config_list},
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config={"use_docker": False},
    system_message="",  # 清空系统消息避免输出
    is_termination_msg=lambda x: True  # 禁用自动终止检测
)

# 原有路由保持不变
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    if not user_message:
        return jsonify({"error": "输入内容不能为空"}), 400

    try:
        # 重置对话历史（可选）
        user_proxy.reset()
        assistant.reset()

        # 发起对话
        user_proxy.initiate_chat(
            assistant,
            message=user_message,
            clear_history=False
        )
        
        # 正确获取最后一条回复
        last_message = user_proxy.last_message(assistant)["content"]
        
        return jsonify({"reply": last_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 其他原有路由...
@app.route("/strategy")
def strategy():
    return render_template("strategy.html")

@app.route("/behavior")
def behavior():
    return render_template("behavior.html")

@app.route("/risk")
def risk():
    return render_template("risk.html")

@app.route("/information")
def information():
    return render_template("information.html")





if __name__ == "__main__":
    app.run(debug=True)
