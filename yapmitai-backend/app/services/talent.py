def get_home() -> dict:
    return {
        "assistants": ["简历优化助手", "技能学习助手", "任务总结助手", "政策咨询助手"],
        "weeklyTasks": 18,
        "savedHours": 7.5,
    }


def call_assistant(assistant: str, prompt: str) -> dict:
    return {"assistant": assistant, "prompt": prompt, "result": f"{assistant}已完成处理。"}
