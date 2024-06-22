from ctransformers import AutoModelForCausalLM
from transformers import pipeline

pipe = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")

llm = AutoModelForCausalLM.from_pretrained("TheBloke/Wizard-Vicuna-7B-Uncensored-GGUF",
                                           model_file="Wizard-Vicuna-7B-Uncensored.Q4_K_M.gguf",
                                           model_type="llama")

dataset_photo_class = ["I want to see you", "I'd like to see your photos", "Send me your photos",
                       "Send me a photo, please", "Do you have a photo? Came", "Can I see your pictures?",
                       "Share your photos", "I want to look at you", "Show me what you look like",
                       "Send me a photo, please", "Is there a chance to see your video?", "I'd like to see your video",
                       "Can you send me a picture?", "Please show me your photos", "I want to watch your videos",
                       "Send me something to look at", "Can you show me your photo?", "I want to see you photos"]


async def nsfw_class(messages):
    result = 0
    filtered_messages = [message for message in messages if message != 'If you want to enjoy all of my exclusive and tantalizing photos, you need to buy them to see every detail']

    for message in filtered_messages:
        res = pipe(message)[0]
        label, score = res['label'], res['score']
        if label == 'NSFW':
            result += score
        else:
            result += 1 - score

    if len(filtered_messages) > 0:
        result /= len(filtered_messages)

    return result > 0.75


async def classifier_text(user_input):
    prompt = f"You have a text in which the user may want to receive photo/video materials. You need to classify it. If the user wants to receive a photo / video, write +, if not, write -. You have to answer this. Do not leave the answer field empty. EXAMPLES: {dataset_photo_class} USER: {user_input}, YOUR_ANSWER:"
    answer = llm(prompt=str(prompt))
    print('class', answer)
    return '+' in answer


async def generate_response(user_input, previous_message):
    user_input += '.'
    script = 'You came after training and you want to tell me about it. How good you feel and want to show your body.'
    prompt = f"You're an alluring and seductive woman working in the adult entertainment industry. You must captivate the user with passionate and erotic communication. Increase the level of arousal and naughtiness with each new message. Your responses should always reflect your female persona and be no more than 300 characters, composed of several sentences. Your interlocutor is a guy. Follow the {script} script. If the dialogue deviates from the script, continue naturally but maintain your persona as a woman. Your previous message was: {previous_message}. Create a new message that is even more provocative and explicit, ensuring you maintain your female character throughout. USER-MAN: {user_input} GIRL: "
    generated_text = llm(prompt=str(prompt))
    print(generated_text)
    return generated_text
