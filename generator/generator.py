import pandas as pd
import random

# 假设三个 Excel 文件分别命名为 tim.xlsx, loc.xlsx, kpi.xlsx 和问句表格 questions.xlsx
tim_df = pd.read_excel("time.xlsx")  # 假设列名为"time"
loc_df = pd.read_excel("location.xlsx")  # 假设列名为"county_name"
kpi_df = pd.read_excel("kpi.xlsx")  # 假设列名为"kpi"
questions_df = pd.read_excel("question.xlsx")  # 假设列名为"question"

# 提取变量值
time_values = tim_df['time'].tolist()
location_values = loc_df['county_name'].tolist()
kpi_values = kpi_df['kpi'].tolist()
question_templates = questions_df['question'].tolist()


def add_tags_to_sentence(template, time_value, location_value, kpi_value):
    def tag_entity(entity, prefix, id_num):
        if not entity:
            return ''
        tagged_entity = [(entity[0], f"B-{prefix}{id_num}")]
        for char in entity[1:]:
            tagged_entity.append((char, f"I-{prefix}{id_num}"))
        return tagged_entity

    # Replace placeholders with tagged entities
    sentence = template.format(tim=time_value, loc=location_value, kpi=kpi_value)

    # Find positions of entities in the sentence
    tim_start = sentence.find(time_value)
    loc_start = sentence.find(location_value)
    kpi_start = sentence.find(kpi_value)

    # Tag entities
    tagged_sentence = []
    current_index = 0

    while current_index < len(sentence):
        if current_index == tim_start:
            tagged_sentence.extend(tag_entity(time_value, 'TIM', time_values.index(time_value) + 1))
            current_index += len(time_value)
        elif current_index == loc_start:
            tagged_sentence.extend(tag_entity(location_value, 'LOC', location_values.index(location_value) + 1))
            current_index += len(location_value)
        elif current_index == kpi_start:
            tagged_sentence.extend(tag_entity(kpi_value, 'KPI', kpi_values.index(kpi_value) + 1))
            current_index += len(kpi_value)
        else:
            tagged_sentence.append((sentence[current_index], 'O'))
            current_index += 1

    return tagged_sentence


# 随机生成 100 个问句
questions = []
for _ in range(20000):
    tim_value = random.choice(time_values)
    loc_value = random.choice(location_values)
    kpi_value = random.choice(kpi_values)
    question_template = random.choice(question_templates)
    tagged_question = add_tags_to_sentence(question_template, tim_value, loc_value, kpi_value)
    questions.append(tagged_question)

doc_name = "train.txt"

# 将生成的问句保存到 question.txt 文件中
with open(doc_name, "w", encoding="utf-8") as file:
    for tagged_question in questions:
        for char, tag in tagged_question:
            if(char != ' '):
                file.write(f"{char} {tag}\n")
        file.write("\n")  # Add a blank line between sentences

print("随机问句已生成，保存为 " + doc_name)


