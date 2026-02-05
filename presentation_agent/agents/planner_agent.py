class PlannerAgent:
    def run(self, slides):
        plan = []

        for slide in slides:
            bullet_count = len(slide["bullets"])
            duration = max(3, bullet_count * 1.5)

            plan.append({
                "title": slide["title"],
                "bullets": slide["bullets"],
                "duration": duration
            })

        return plan
