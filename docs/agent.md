# 🧠 Agent Class — Intelligent Tool-Using LLM Agent

## 📘 خلاصه

کلاس `Agent` نماینده یک موجودیت هوشمند بر پایه LLM است که می‌تواند:

* بر اساس یک سیستم پرامپت (prompt) فکر کند و پاسخ دهد
* متدهای داخلی خودش را به عنوان «ابزار» معرفی کند
* با استفاده از ابزارها، عملکردهای پیچیده‌تری انجام دهد
* در صورت نیاز از مدل زبانی برای انتخاب، تحلیل و تصمیم‌گیری استفاده کند

---

## ✅ کاربرد اصلی

* تعریف Agentهای تخصصی با ابزارهای اختصاصی (با متدهای ساده)
* تبدیل هر Agent به یک LLMChain با قابلیت تعامل متنی
* استفاده از ابزارها با ساختار JSON برای اجرای دستورات خاص
* تصمیم‌گیری بر اساس انتخاب از میان گزینه‌ها

---

## ⚙️ سازنده

```python
def __init__(self, mainText: str, modelName: str, maxRetray=3, baseUrl="http://localhost:11434")
```

| پارامتر     | توضیح                                                    |
| ----------- | -------------------------------------------------------- |
| `mainText`  | توضیح نقش Agent، به عنوان بخش اصلی system prompt         |
| `modelName` | نام مدل LLM برای پاسخ‌دهی (مثل `mistral`, `llama3`, ...) |
| `maxRetray` | حداکثر تعداد تلاش برای گرفتن پاسخ درست هنگام انتخاب      |
| `baseUrl`   | آدرس سرویس LLM (پیش‌فرض: ollama لوکال)                   |

---

## 🧩 اجزای اصلی

### 🔸 `self.chain`

یک زنجیره LangChain که شامل:

1. `PromptTemplate` با system prompt + سؤال
2. `OllamaLLM` مدل زبانی
3. (اختیاری) `JsonOutputParser` + ابزارهای داخلی

---

### 🔸 `self._tools`

ابزارهایی هستند که از طریق متدهای کلاس (بدون underscore و بدون override از init) شناسایی می‌شوند و با دکوراتور `@tool` بسته‌بندی می‌شوند.

---

## 🔧 متدهای مهم

### `message(message: str) -> str`

پاسخ ساده‌ی LLM به یک سؤال:

```python
agent.message("سلام چطوری؟")
```

---

### `select(text: str, options: list | dict, think=False) -> str | None`

یک گزینه را با کمک LLM از بین گزینه‌ها انتخاب می‌کند.

```python
agent.select("کدام عدد اول است؟", ["9", "7", "10"])
# یا
agent.select("کدام Agent مناسب‌تر است؟", {"0": "ریاضی", "1": "چت"})
```

* اگر `think=True` باشد، در صورت پاسخ نامعتبر، تلاش دوباره می‌کند.

---

### `_invoke_tool(tool_call_request: ToolCallRequest) -> Any`

اجرای یک ابزار با ساختار JSON:

```python
agent._invoke_tool({
    "name": "calculate_sum",
    "arguments": {"a": 3, "b": 5}
})
```

* به طور خودکار بین ابزارهای داخلی جستجو می‌کند.
* اگر ابزاری با آن نام پیدا نشود، `"function not found"` بازمی‌گرداند.

---

### `_descibe_yourself() -> str`

یک توصیف متنی از Agent و سیستم پرامپت آن را بازمی‌گرداند. برای استفاده توسط Orchestration کاربرد دارد.

---

### `@property _tools`

بازگرداندن ابزارهای داخلی کلاس. متدهایی که:

* با \_ شروع نمی‌شوند
* در `__dict__` نباشند
* در `self._ignoreFuncs` نباشند
  به صورت ابزار درنظر گرفته می‌شوند.

---

## 🧪 تعریف ابزار (Tool)

برای اضافه‌کردن ابزار به Agent، کافی است یک متد تعریف کنید بدون underscore، مثلاً:

```python
def say_hello(self, name: str) -> str:
    return f"Hello {name}"
```

این متد به صورت خودکار در Agent به عنوان ابزار قابل فراخوانی خواهد بود و در prompt نیز معرفی می‌شود.

برای اینکه هوش مصنوعی از این ابزار استفاده کند باید فانکشن رو داخل کلاس بنویسد.

---

## 🛡️ ویژگی‌های دیگر


## 📎 وابستگی‌ها

* `langchain`
* `langchain_ollama`
* `Ollama` backend فعال (لوکال یا remote)

---

## ✨ نمونه استفاده

```python
from aaaai.agent import Agent


class MathAgent(Agent):

    # اضافه‌کردن ابزار دلخواه به کلاس Agent
    def calculate(self, x: int, y: int) -> int:
        """this function sum two numbers"""
        return x + y


agent = MathAgent("You are a math assistant.", modelName="mistral")

# پاسخ گرفتن از طریق پیام ساده
print(agent.message("Hi, what is 2+2?"))

# یا با ابزار (مثلاً از طریق JsonOutputParser)
response = agent.message("Please use the calculate tool to add 3 and 5.")
print(response)
```

