class TokenOptimizer:
    @staticmethod
    def calculate_approx_tokens(text: str) -> int:
        """Helper to calculate approximate token count (ratio: 4 chars = 1 token)."""
        return len(text) // 4

    @staticmethod
    def compress_tool_output(output_str: str, max_chars=1500) -> str:
        """Crops large tool output logs (such as HTML page scrapings) to prevent context flooding."""
        if len(output_str) <= max_chars:
            return output_str
        return f"{output_str[:max_chars]}\n... [Tool Output Truncated by TokenOptimizer ({len(output_str) - max_chars} characters removed)]"

    @staticmethod
    def optimize_messages(messages: list, max_tokens=2500) -> list:
        """
        Optimizes LLM message arrays before execution.
        Iterates backwards and discards older message records once token thresholds are reached.
        """
        optimized = []
        token_count = 0
        
        # Iterate backwards to preserve most recent messages
        for msg in reversed(messages):
            content = msg.get("content", "") if isinstance(msg, dict) else getattr(msg, "content", "")
            approx_tok = TokenOptimizer.calculate_approx_tokens(content)
            
            # If adding this message exceeds the threshold, skip older ones
            if token_count + approx_tok > max_tokens:
                print(f"TokenOptimizer: Discarded older messages. Retained {len(optimized)} items.")
                break
                
            optimized.insert(0, msg)
            token_count += approx_tok
            
        return optimized
