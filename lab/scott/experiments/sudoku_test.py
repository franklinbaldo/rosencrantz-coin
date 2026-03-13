import json

from litellm import completion


def check_sudoku(grid):
    """Checks if a 9x9 Sudoku grid is valid."""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False

    # Check rows and cols
    for i in range(9):
        row_vals = [x for x in grid[i] if x != 0]
        col_vals = [grid[j][i] for j in range(9) if grid[j][i] != 0]
        if len(set(row_vals)) != len(row_vals) or len(set(col_vals)) != len(col_vals):
            return False

    # Check 3x3 blocks
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block_vals = [
                grid[x][y] for x in range(i, i + 3) for y in range(j, j + 3) if grid[x][y] != 0
            ]
            if len(set(block_vals)) != len(block_vals):
                return False

    return True


def mock_litellm_completion(model, messages, **kwargs):
    """Mocks litellm response if OPENAI_API_KEY is not available."""
    prompt = messages[-1]["content"]

    # Simple deterministic failure logic for testing constraint satisfaction
    if "Level: Easy" in prompt:
        return type(
            "obj",
            (object,),
            {
                "choices": [
                    type("obj", (object,), {"message": type("obj", (object,), {"content": "7"})})
                ]
            },
        )
    elif "Level: Medium" in prompt:
        return type(
            "obj",
            (object,),
            {
                "choices": [
                    type("obj", (object,), {"message": type("obj", (object,), {"content": "3"})})
                ]
            },
        )
    else:
        # Fails hard constraints
        return type(
            "obj",
            (object,),
            {
                "choices": [
                    type("obj", (object,), {"message": type("obj", (object,), {"content": "9"})})
                ]
            },
        )


def test_llm_sudoku_constraint():
    try:
        import os

        if not os.environ.get("OPENAI_API_KEY"):
            print("No OPENAI_API_KEY found, using mock completion.")
            generate = mock_litellm_completion
        else:
            generate = completion
    except Exception as e:
        print(f"Error setting up litellm: {e}")
        return

    boards = [
        # Easy: Only 1 cell missing (determinisitc)
        {
            "difficulty": "Easy",
            "grid": [
                [5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 0],  # Missing last cell (should be 9)
            ],
            "target": (8, 8),
            "expected": 9,
        },
        # Hard: Almost empty board
        {
            "difficulty": "Hard",
            "grid": [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9],
            ],
            "target": (0, 2),
        },
    ]

    results = []

    for board in boards:
        difficulty = board["difficulty"]
        grid = board["grid"]
        target_r, target_c = board["target"]

        prompt = f"Solve the following Sudoku board cell. Level: {difficulty}\n"
        for row in grid:
            prompt += " ".join(str(x) if x != 0 else "." for x in row) + "\n"
        prompt += f"\nWhat number belongs in row {target_r + 1}, column {target_c + 1}? Answer with just a single digit (1-9)."

        response = generate(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], temperature=0
        )

        predicted_val_str = response.choices[0].message.content.strip()
        try:
            predicted_val = int(predicted_val_str)
        except Exception:
            predicted_val = -1

        # Check constraint satisfaction dynamically
        grid[target_r][target_c] = predicted_val
        is_valid = check_sudoku(grid)

        result = {
            "difficulty": difficulty,
            "predicted": predicted_val,
            "is_valid_constraint": is_valid,
        }
        if "expected" in board:
            result["expected"] = board["expected"]
            result["correct"] = predicted_val == board["expected"]

        results.append(result)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    test_llm_sudoku_constraint()
