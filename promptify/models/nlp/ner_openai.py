# from openai import OpenAI
from openai import AsyncOpenAI


class NERLabeler:
    def __init__(self, api_key, labels, mode='NER_cv_vi', model: str = "gpt-3.5-turbo") -> None:
        self.model = model
        self.mode = mode
        self.client = AsyncOpenAI(api_key=api_key)
        self.message = [
            {"role": "system", "content": self.system_message(labels=labels)},
            {"role": "assistant", "content": self.assisstant_message()},
            {"role": "user", "content": self.user_message(text='')}
        ]

    def system_message(self, labels):
        if self.mode == 'NER_cv_vi':
            return NER_cv_vi_system_message + f"({', '.join(labels)})."
        elif self.mode == 'NER_cv_eng':
            return NER_cv_eng_system_message + f"({', '.join(labels)})."
        return 

    def assisstant_message(self):
        if self.mode == 'NER_cv_vi':
            return NER_cv_vi_assisstant_message
        elif self.mode == 'NER_cv_eng':
            return NER_cv_eng_assisstant_message
        return 

    def user_message(self, text):
        return f"""
    TASK:
        Text: {text}
    """

    async def request(self, text):
        self.message[-1] = {"role": "user", "content": self.user_message(text=text)}
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=self.message,
            temperature=0,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content


NER_cv_vi_system_message = f"""
    You are an expert in Natural Language Processing. Your task is to identify common Named Entities (NER) in a given text.
    The possible common Named Entities (NER) types are exclusively: """

NER_cv_eng_system_message = f"""
    You are an expert in Natural Language Processing. Your task is to identify common Named Entities (NER) in a given text.
    The possible common Named Entities (NER) types are exclusively: """

NER_cv_vi_assisstant_message = f"""
    EXAMPLE:
        {{
            "CV_role": ["FRESHER DEVELOPER - PHP"],
            "Personal_name": ["Lê Xuân Tiến"],
            "Personal_Birthdate": ["25/10/1997"],
            "Personal_Phonenumber": ["0932 311 434"],
            "Personal_Email": ["tienlx97@gmail.com"],
            "Personal_Address": ["Xuân Thới Thượng, Hóc Môn, Hồ Chí Minh"],
            "Personal_Website": ["https://www.facebook.com/tienlx97", "github.com/tienlxv"],
            "University_Name": ["Trường Đại học Công nghệ Thông tin ĐHQG TP.HCM"],
            "Education_Major": ["Công nghệ phần mềm"],
            "Education_Duration": ["8/2015 - nay"],
            "Education_GPA": ["7.3"],
            "Technical_skills_Programing_language": ["Java", "C#", "java script", "php", "python", "C", "C++", "html", "css"],
            "Technical_skills_Framework": ["Django", "React.js", "Spring Boot", "Angular", "React Native", "Node JS", "Express Js", "Java Fx", "Unity", "Libgdx"],
            "Other_Technical_skills_Knowlage":["Java core", "design pattern", "Git"],
            "Technical_skills_Platform":["AWS", "Microsoft Azure", "GCP", "Docker"],
            "Technical_skills_Tool":["Unity", "Eclipse", "Android Studio", "Github", "Jira", "Postman", "Figma", "Adobe XD", "Photoshop"]
            "Soft_skill": ["Làm việc nhóm", "Khả năng tư duy và sáng tạo"],
            "Work_experience_Comapany_Name": ["QSoft Việt Nam", "TMA Solutions", "Netcompany"],
            "Work_experience_Comapany_Duration":["2016-2017","2017","7/2017-8/2018"],
            "Work_experience_Comapany_Role_and_Responsibilitie": ["Thiết kế database", "Phân tích, phát triển module", "Thiết kế framework"],
            "Foreign_language_certificate":["TOEIC: 760"],
            "Technical_certificate":["AWS Certified Solutions Architect - Associate (SAA-C03)"]
        }}
    --"""

NER_cv_eng_assisstant_message = f"""
    EXAMPLE:
        {{
        "CV_role": ["FRESH DEVELOPER - PHP"],
        "Personal_name": ["Le Xuan Tien"],
        "Personal_Birthdate": ["October 25, 1997"],
        "Personal_Phonenumber": ["0932 311 434"],
        "Personal_Email": ["tienlx97@gmail.com"],
        "Personal_Address": ["Xuan Thoi Thuong, Hoc Mon, Ho Chi Minh"],
        "Personal_Website": ["https://www.facebook.com/tienlx97", "github.com/tienlxv"],
        "University_Name": ["Ho Chi Minh City University of Information Technology"],
        "Education_Major": ["Software Engineering"],
        "Education_Duration": ["August 2015 - Present"],
        "Education_GPA": ["7.3"],
        "Technical_skills_Programing_language": ["Java", "C#", "JavaScript", "PHP", "Python", "C", "C++", "HTML", "CSS"],
        "Technical_skills_Framework": ["Django", "React.js", "Spring Boot", "Angular", "React Native", "Node JS", "Express Js", "Java Fx", "Unity", "Libgdx"],
        "Other_Technical_skills_Knowlage": ["Java Core", "Design Patterns", "Git"],
        "Technical_skills_Platform": ["AWS", "Microsoft Azure", "GCP", "Docker"],
        "Technical_skills_Tool": ["Unity", "Eclipse", "Android Studio", "GitHub", "Jira", "Postman", "Figma", "Adobe XD", "Photoshop"],
        "Soft_skill": ["Teamwork", "Thinking and creativity"],
        "Work_experience_Comapany_Name": ["QSoft Vietnam", "TMA Solutions", "Netcompany"],
        "Work_experience_Comapany_Duration": ["2016-2017", "2017", "July 2017 - August 2018"],
        "Work_experience_Comapany_Role_and_Responsibilitie": ["Database design", "Module analysis and development", "Framework design"],
        "Foreign_language_certificate": ["TOEIC: 760"],
        "Technical_certificate": ["AWS Certified Solutions Architect - Associate (SAA-C03)"]
        }}
    --"""


