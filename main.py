import sys
import time
from utills.file_utils import read_file, validate_file
from openai import OpenAI
from models.resume_models import *
import json
from config.config import *
from models.template import  system_prompt
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
pdf_file_path="./Resumes/resume.pdf"
file_basename = os.path.basename(pdf_file_path)
is_valid, message = validate_file(pdf_file_path)
if not is_valid:
    print(f"Validation failed for {file_basename}: {message}")
    # return None


extracted_text = read_file(pdf_file_path)
user_prompt = f"""
Parse the following resume text into JSON objects matching the Pydantic models:

- ResumeProfile
- ResumeSkills
- ResumeEducation
- ResumeWorkExperience
- Resume (full resume)

Resume Text:
{extracted_text}
"""
start=time.time()
response = client.chat.completions.create(
    model=DEFAULT_LLM_MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=LLM_TEMPERATURE
)
print(time.time()-start)

def main():
    """Main entry point."""
    try:
        parsed_json = response.choices[0].message.content
        parsed_data = json.loads(parsed_json)
        profile = ResumeProfile.model_validate(parsed_data.get("profile"))
        skills = ResumeSkills.model_validate(parsed_data.get("skills", []))
        education = Education.model_validate(parsed_data.get("education", {}))
        raw_work_experience = parsed_data.get("work_experience", [])
        for item in raw_work_experience:
            if "position" in item:
                item["role"] = item.pop("position")
        work_experience = ResumeWorkExperience.model_validate({
            "work_experiences": raw_work_experience
        })
        full_resume = Resume.model_validate({"full_resume": parsed_data.get("full_resume", "")})
        print("profile:", profile, "skills:", skills, "education:", education, "work_experience:", work_experience,
              "full_resume:", full_resume)

    except Exception as e:
        print("Exception {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()

