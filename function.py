import json
from prompts import summary_prompt
from models import summary_model
import os
from dotenv import load_dotenv
load_dotenv()
import pymysql

db = pymysql.connect(
    host=os.getenv("HOST"),
    port=3306,
    user=os.getenv("USER"),
    passwd=os.getenv("PASSWD"),
    db=os.getenv("DB"),
    charset='utf8',
    autocommit=True
)

def summarization(memory : list, trigger : int = 16, keep : int = 2, system_prompt : str = summary_prompt) :
    if len(memory) >= trigger:
        response = summary_model.invoke(
            [{"role": "system", "content": f"{system_prompt}"}] + memory[:-keep] + [{"role": "user", "content": f"지금까지 나눈 대화를 요약해줘"}]
        )
        return [{'role':'user','content':response.content}]
    else:
        return memory

def get_memory(conversation_id : int = 1, drawing_id : int = 1) -> list:
    db.ping(reconnect=True)
    memory = []
    try:
        cursor = db.cursor()

        read_sql = "SELECT * FROM CONVERSATION WHERE id = %s AND drawing_id = %s"
        cursor.execute(read_sql, (conversation_id, drawing_id))
        row = cursor.fetchone()
        print(row)
        if row[-1]:
            memory = json.loads(row[-1])['messages']
        else:
            update_sql = "UPDATE CONVERSATION SET message = %s WHERE id = %s AND drawing_id = %s"
            cursor.execute(update_sql,
                           (json.dumps({'messages': []}, indent=2, ensure_ascii=False), conversation_id,
                            drawing_id))
            db.commit()

    except Exception as e:
        print(f"에러 발생: {e}")

    finally:
        cursor.close()
    print(memory)
    return memory

def send_memory(conversation_id : int, drawing_id : int, messages : list) :
    db.ping(reconnect=True)
    try:
        cursor = db.cursor()
        update_sql = "UPDATE CONVERSATION SET message = %s WHERE id = %s AND drawing_id = %s"
        cursor.execute(update_sql, (json.dumps({'messages':messages}, indent=2, ensure_ascii=False), conversation_id, drawing_id))
        db.commit()

    except Exception as e:
        print(f"에러 발생: {e}")
        db.rollback()

    finally:
        cursor.close()

    return
