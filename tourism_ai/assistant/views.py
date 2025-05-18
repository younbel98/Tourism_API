import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tools import tool_definitions, execute_tool
from .memory import get_user_messages, save_user_message

OPENROUTER_API_KEY = (
    "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"
)
REFERER_HEADER = "http://localhost:8000"  # or "http://localhost:8000"


@csrf_exempt
def chat_handler(request):
    data = json.loads(request.body)
    user_id = data.get("user_id")
    message = data.get("message")

    save_user_message(user_id, "user", message)
    messages = get_user_messages(user_id)
    tools = tool_definitions()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": REFERER_HEADER,
        "X-Title": "Tourism Assistant",
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # or another available model from OpenRouter
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto",
    }

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        res.raise_for_status()
        result = res.json()

        message_out = result["choices"][0]["message"]
        save_user_message(user_id, message_out["role"], message_out.get("content", ""))

        if "tool_calls" in message_out:
            results = []
            for call in message_out["tool_calls"]:
                tool_name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                tool_result = execute_tool(user_id, tool_name, args)
                results.append({"tool": tool_name, "result": tool_result})
            return JsonResponse({"tool_calls": results})

        return JsonResponse({"response": message_out.get("content", "")})

    except requests.RequestException as e:
        return JsonResponse(
            {"error": "API connection failed", "detail": str(e)}, status=500
        )
    except Exception as e:
        return JsonResponse({"error": "Internal error", "detail": str(e)}, status=500)
