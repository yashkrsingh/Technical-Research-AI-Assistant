from string import Template

class OrchestratorPrompts:

    TASK_DECOMPOSER_USER_PROMPT = Template(
        """
        You are a senior software architect.
        Break the following provided engineering task down into clear technical subtasks 
        
        TASK
        ---
        
        "$user_query"
        
        OUTPUT FORMAT
        ---
        
        Return ONLY a JSON array of strings
        
        EXAMPLE OUTPUT
        ---
        
        [
            "Identify suitable recommendation algorithms",
            "Determine required data sources",
            "Define system architecture",
            "Select evaluation metrics",
            "Plan deployment strategy"
        ]

        """
    )


    RESEARCH_PLANNER_USER_PROMPT = Template(
        """
        Given a list of subtasks, generate research queries that will help design the system.
        
        SUBTASKS
        ---
        
        "$sub_task_list"
        
        OUTPUT FORMAT:
        ---
        
        [
            "Collaborative filtering vs content-based filtering",
            "Deep learning recommenders e-commerce",
            "Cold start problem solutions",
            "Scalable recommendation architectures"
        ]
        
        Return ONLY a JSON array of strings containing research queries
        
        """
    )

    APPROACH_COMPARATOR_SYSTEM_PROMPT = Template(
        """
        Using the research topics, list viable technical approaches.

        RESEARCH
        ---
        
        $research_topics"
        
        RELEVANT WEB SEARCH DOCUMENTS
        ---
        
        $relevant_docs
        
        ""
        
        For each approach, include:
        - approach
        - pros
        - cons
        - best_for
        
        
        OUTPUT FORMAT
        ---
        
        [
          {
            "approach": "Collaborative Filtering",
            "pros": [...],
            "cons": [...],
            "best_for": "Large user-item interaction data"
          }
        ]
        
        Return ONLY a JSON array of objects as per the given example format
        
        """
    )

    SOLUTION_SYNTHESIZER_PROMPT = Template(
        """
        Given the following approaches, select the most appropriate one
        for a real-world production system.
        
        APPROACHES
        ---
        
        $approaches
        
        Explain reasoning and return JSON account to the following format
        {
          "recommended_approach": {...},
          "reasoning": "..."
        }
        
        Return only a JSON object
        """
    )

    STRUCTURED_PLAN_GENERATOR_PROMPT = Template(
        """
        Based on the selected approach below, generate a structured
        technical implementation plan.
        
        Approach:
        $selected_approach
        
        Return JSON with:
        - architecture
        - tech_stack
        - risks
        - timeline
        
        """
    )