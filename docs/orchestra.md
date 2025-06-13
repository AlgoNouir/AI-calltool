
# 🧠 Orchestration Class — Agent Collaboration Layer

## 📘 توضیح کلی

کلاس `Orchestration` بخشی از سیستم چندعامله‌ی شماست که با هدف **اتصال و مدیریت Agentهای مختلف** طراحی شده است. این کلاس یک Agent مستقل نیز هست، و با استفاده از مدل‌های زبان (مثل LLM)، بهترین Agent را برای انجام یک وظیفه خاص انتخاب می‌کند و تعامل را هدایت می‌کند.

---

## ✅ کاربرد اصلی

* ثبت Agentهای مختلف با توصیف قابلیت‌هایشان
* انتخاب هوشمندانه بهترین Agent برای هر درخواست
* ارسال پیام (Prompt) به آن Agent و دریافت پاسخ
* لایه میانی بین کاربر و سیستم Agentها

---

## 🧱 ساختار کلاس

```python
class Orchestration(Agent):
```

کلاس `Orchestration` از کلاس پایه `Agent` ارث‌بری می‌کند و به همین دلیل قابلیت تعامل زبانی (مثلاً با LLM) را نیز دارد.

---

## ⚙️ پارامترهای سازنده

```python
def __init__(self, modelName, maxRetray=3, baseUrl="http://localhost:11434"):
```

| پارامتر     | توضیح                                      |
| ----------- | ------------------------------------------ |
| `modelName` | نام مدل LLM مورد استفاده در Agent مادر     |
| `maxRetray` | تعداد تلاش مجدد در صورت خطا                |
| `baseUrl`   | آدرس سرویس LLM (مثل ollama یا یک API محلی) |

---

## 🔐 ویژگی‌ها

### 🧠 `self.agents: dict[Agent, str]`

* نگهدارنده‌ی Agentهای ثبت‌شده.
* هر Agent با توضیح توانمندی‌هایش (`_descibe_yourself()`) در دیکشنری ذخیره می‌شود.

---

## 🔧 متدها

### `register(agent: Agent)`

ثبت یک Agent جدید در سیستم:

```python
def register(self, agent: Agent) -> None:
```

* فراخوانی `agent._descibe_yourself()` برای استخراج توصیف توانمندی‌ها.
* Agent و توصیف آن در `self.agents` ذخیره می‌شود.

---

### `selectAgent(desier: str) -> Agent`

انتخاب هوشمندانه‌ی بهترین Agent برای یک وظیفه:

```python
def selectAgent(self, desier: str) -> Agent:
```

* با استفاده از مدل زبانی (LLM) از بین Agentهای ثبت‌شده انتخاب می‌کند.
* سؤال از مدل: «کدام Agent برای این وظیفه مناسب است؟»
* پاسخ مدل به صورت index بازگردانده می‌شود.
* خروجی: یک نمونه از کلاس `Agent`.

---

### `invoke(desier: str) -> str`

متد اصلی برای دریافت پاسخ از سیستم:

```python
def invoke(self, desier: str) -> str:
```

* ابتدا `selectAgent` را برای یافتن Agent مناسب فراخوانی می‌کند.
* سپس پیام را به آن Agent ارسال می‌کند و پاسخ را باز می‌گرداند.

---

## 🚫 @property `_ignoreFuncs`

```python
@property
def _ignoreFuncs(self):
```

لیستی از متدهایی که نباید توسط Agent مادر (مثلاً در پاسخ‌دهی خودکار) استفاده شوند. شامل:

* `register`
* `invoke`
* `selectAgent`
* توابع پایه‌ی کلاس مادر

---

## 📌 نحوه استفاده (Usage)

```python
# تعریف یک ارکستراسیون
orch = Orchestration(modelName="mistral")

# ثبت Agentها
orch.register(math_agent)
orch.register(chat_agent)

# پردازش یک درخواست کاربر
response = orch.invoke("لطفاً ۱۲ * ۳ را محاسبه کن")
print(response)
```

---

## 🧩 قابلیت‌های قابل گسترش (Ideas)

| قابلیت پیشنهادی                                | توضیح                                 |
| ---------------------------------------------- | ------------------------------------- |
| استفاده از امتیاز (scoring) به‌جای انتخاب واحد | مثلاً top-k agent و vote کردن         |
| نگهداری تاریخچه گفتگوها                        | برای حفظ context و بررسی لاگ‌ها       |
| async بودن برای scale بالا                     | با استفاده از `async def` و `asyncio` |
| مدل route مرکزی (مثل `router LLM`)             | انتخاب Agent با مدل زبان جداگانه      |

---

## 📎 وابستگی‌ها

* `aaaai.agent.Agent`: کلاس پایه‌ی Agent شما
* یک backend مثل Ollama یا سرویس LLM لوکال برای پاسخ‌دهی

---

## 📝 توضیح فنی `select(...)`

```python
selectedIndex = self.select(prompt, options_dict)
```

* این تابع از کلاس مادر به ارث می‌رسد و برای **انتخاب یکی از گزینه‌ها با کمک LLM** استفاده می‌شود.
* `options_dict` باید دیکشنری `{index: description}` باشد.
* خروجی `selectedIndex` به صورت string (مثلاً `"0"`) بازگردانده می‌شود.
