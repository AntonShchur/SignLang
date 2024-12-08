from langchain_openai import ChatOpenAI, OpenAI
from langchain_ollama import ChatOllama
from constants_translation import sentence_lang_to_sign_cache
from dotenv import load_dotenv
import enum
load_dotenv()

class SentenceType(enum.Enum):
    declarative = "declarative"
    interrogative = "interrogative"
    exclamatory = "exclamatory"
    imperative = "imperative"
    

class LangToSign:
    __models = {"gpt-4o":ChatOpenAI,
                "gpt-4o-mini":ChatOpenAI,
                "llama3.1:latest":ChatOllama}
    
    __check_sentence_type_prompt = """
        Ти помічниу у визначенні типу речення. Поверни відповідний тип речення українській мові використовуючи одну з доступних відповідей "declarative", "interrogative", "imperative", "exclamatory"
        Тобі треба визначити до якого типу з перелічених у дужках (розповідне, питальне, заперечне) 
        є наступне речення. Воно написане українською мовою.
        Речення для аналізу:
        "{}"
        \n
        Якщо речення є розповідним, то поверни "declarative"
        Якщо речення є питальним, то поверни "interrogative"
        Якщо речення є заперечним, то поверни "imperative"
        Якщо речення є спонукальним, то поверни "exclamatory"
        Більше не повертай нічого, лише тип речення, не повертай інших типів, окрім як [declarative, interrogative, imperative, exclamatory]
        """
        
    __rules_explanatory = """
        Правило 1
        При побудові розповідного речення першим відтворюється підмет, потім
        присудок і додаток (спочатку відтворюється прямий додаток, а потім непрямий).
        
        Отже, структурна схема такого речення виглядатиме так: Sub + Pred + Obj + InObj. 
        
        Дієслова у формі майбутнього часу переходять у неозначену форму дієслова (інфінітив) та виключно після них додається допоміжне слово "буду". Наприклад слово "житиму" перкладається як "жити буду"
        Дієслова у формі минулого часу переходять у неозначену форму дієслова (інфінітив) та вилючно після них додається допоміжне слово "був". Наприклад слово "жив" перекладається як "жити був"
        Дієслова у формі тепершішнього часу переходять у неозначену форму дієслова (інфінітив) та після них ніяких лопоміжних слів не додається. Наприклад "живу", перекладається як "жити"
        

        Правило 2
        У простому розповідному стверджувальному реченні спочатку відтворюється
        іменник, тоді прикметник, тобто, спочатку – “хто”, а потім  “який”. У випадку наявності двох і
        більше прикметників вони відтворюються послідовно. 
        При перекладі з УСМ УЖМ прикметник у знахідному відмінку (та у всіх інших) однини
        (множини) чоловічого (жіночого, середнього) роду переходить у форму називного відмінка однини
        (множини) (Adj(s m c4) → Adj(s)).
        
        Правило 3
        При побудові речення прислівники
        використовуються після тих слів, до яких вони стосуються.
        Прислівники місця, часу, мети, причини, способу дії в українській мові після перекладу
        на українську жестову мову не змінюються.
        
        Правило 4
        При побудові будь-якого речення, якщо в ньому присутні слова, що позначають множину, то такі слова заміняються двома словами однини, наприклад слово "собаки" на "собака собака"
    """
    
    __rules_interrogative = """
        Правило 5
        В українській мові жестів для побудови питального речення застосовують таке правило: питальні
        слова (наприклад, “як”, “коли”, “чому”, “скільки”), завжди ставляться в кінці речення.
    """
    
    __rules_negative = """
        Правило 6
        В українській мові жестів заперечні одиниці “ні”, “не буде”, “ніколи”,
        не хочу” тощо, які є основою розповідних заперечних жестових конструкцій, застосовуються лише
        після жестів, які вони заперечують.
        Одиниці словесної, які несуть в собі заперечення, в УЖМ, при можливості, замінюються не
        відповідними, а іншими жестами. Наприклад, “не дорогий” – “дешевий”, “не весело” – “сумно”.
        Якщо “не” ставиться після певного слова, наприклад, “не мій”, то його показують як “мій + не”.
    """
    
    
    def __init__(self, model="gpt-4o-mini", temperature=0.8):
        if model in LangToSign.__models.keys():
            self.llm: ChatOpenAI = LangToSign.__models[model](model=model, temperature=temperature)
    
    
    def define_sentence_type(self, sentence:str) ->SentenceType: 
        message = self.__check_sentence_type_prompt.format(sentence)
        result = self.llm.invoke(message)
        match result.content:
            case "declarative":
                return SentenceType.declarative
            case "interrogative":
                return SentenceType.interrogative
            case "imperative":
                return SentenceType.imperative
            case "exclamatory":
                return SentenceType.exclamatory
        
        
    def translate_sentence(self, sentence:str) -> str:
        sentence_type = self.define_sentence_type(sentence)
        if sentence in sentence_lang_to_sign_cache.keys():
            return sentence_lang_to_sign_cache[sentence]
        if sentence_type == SentenceType.declarative or sentence_type == SentenceType.exclamatory:
            print(SentenceType.declarative)
            prompt = """
            Зараз ти будеш перекладати розповідне речення з української мови на українську мову жестів застосовуючи наступні правила:
            {}
            Дотримуйся цих правил та застосовую всі свої знання з семантичного розбору речення. Переклади наступне речення за заданими вище правилами
            {}
            Поверни лише перекладене речення, уникай пояснень.
            """
            sentence_to_translate = prompt.format(self.__rules_explanatory, sentence)
            result = self.llm.invoke(sentence_to_translate)
            return result.content
        
        elif sentence_type == SentenceType.interrogative:
            print(SentenceType.interrogative)
            prompt = """
            Зараз ти будеш перекладали питальне речення з української мови на українську мову жестів застосовуючи наступні правила:
            {}
            \n
            {}
            Переклади речення, що я тобі надам, застосовуючи правила, що я тобі надав вище. Оброблюй речення поступово, пройдись по кожному правилу і застосуй його за потреби.
            Речення для перекладу
            {}
            Поверни лише перекладене речення, уникай пояснень.           
            """
            sentence_to_translate = prompt.format(self.__rules_explanatory, self.__rules_interrogative, sentence)
            result = self.llm.invoke(sentence_to_translate)
            return result.content
            
            
        elif sentence_type == SentenceType.imperative:
            print(SentenceType.imperative)
            prompt = """
            Зараз ти будеш перекладали розповідне  речення з української мови на українську мову жестів застосовуючи наступні правила:
            {.GenralRules}
            \n
            {.RulesForExplanation}
            Переклади речення, що я тобі надам, застосовуючи правила, що я тобі надав вище. Оброблюй речення поступово, пройдись по кожному правилу і застосуй його за потреби.
            Наприклад:
            "Сьогодні була гарна та сонячна погода" буде перекладатись на можу жестів як "Сьогодні погода був гарний та сонячний"
            Речення для перекладу
            {.Input}
            Поверни лише перекладене речення, уникай пояснень.  
            {.Output}   
            """
            sentence_to_translate = prompt.format(self.__rules_interrogative, self.__rules_negative, sentence)
            result = self.llm.invoke(sentence_to_translate)
            return result.content
        else:
            raise TypeError(f"Sentence Type should be in { [SentenceType.imperative, SentenceType.exclamatory, SentenceType.interrogative, SentenceType.declarative]}")
        
            
if __name__ == "__main__":
    lang_to_sign = LangToSign()
    sentence_result = {
        "Чи може вовк злякати кролика?":"",
        "Коли сьогодні ми підемо у кафе?":"",
        "Якого кольору твій улюблений велосипед?":"",
        "Яка твоя улюлена пісня?":"",
        "Чому дитина плаче?":""
    }
    
    for key in sentence_result.keys():
        sentence_to_test = key
        result = lang_to_sign.translate_sentence(sentence_to_test)
        print(f"{key}: {result}")