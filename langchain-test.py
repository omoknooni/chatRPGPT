from langchain.schema import HumanMessage, SystemMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "GOOGLE_API_KEY"

response_scheme = {
    "title": "Story",
    "description": "The story of the game",
    "type": "object",
    "properties": {
        "story": {
            "type": "string",
            "description": "The story of the game"
        },
        "choices": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "The options for the player"
            }
        }
    },
    "required": ["story", "choices"],
}

# class response_scheme(BaseModel):
#     story: str = Field(description="The story of the game")
#     choices: list[str] = Field(description="The options for the player")

# gemini-1.5-flash 모델은 structured output 미지원 (response 빈값)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
structured_llm = llm.with_structured_output(response_scheme)

def main():
    quest = "Defeating the dragon that is located in the deepest floor of the Dungeon"
    word_limit = 50
    protagonist_name = "John, who is excellence in swordsmanship and archery skill"
    storyteller_name = "Dungeon Master"

    is_start = True
    is_end = False
    selection = ""

    # 초기 game 설정문
    game_description = f"""Here is the topic for a Table Roleplay game: {quest}.
            There is one player in this game: the protagonist, {protagonist_name}.
            The story is narrated by the storyteller, {storyteller_name}."""

    while not is_end:
        if is_start:
            story_instuction = "Please make the beginning of the story based on the topic."
        else:
            story_instuction = f"""Based on the previous stories, situations and player's choice, please continue to write the next situation in this story.
            The player choiced '{selection}'"""

        # GM의 진행 프롬프트, 진행상황 묘사 및 player가 선택할 수 있는 option 제공
        content_prompt = f"""{game_description}
        You are the storyteller, {storyteller_name}.
        {story_instuction} Write the Story in {word_limit} words or less.
        And also create 2~3 options for that situation. Then, reply these options.
        Do not add anything else."""

        generated_story = structured_llm.invoke(content_prompt)[0]["args"]
        story = generated_story["story"]
        options = generated_story["choices"]
        # print(generated_story)
        # print("=================================================")
        print(f"GM >>> {story}")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        while True:
            players_choice = input(f"Enter your choice (1~{len(options)}): ")
            if players_choice.isdigit() and 1 <= int(players_choice) <= len(options):
                break
            else:
                print("Invalid input. Please enter a number within the range.")
        is_start = False

        selection = options[int(players_choice)-1]
    


if __name__ == "__main__":
    main()