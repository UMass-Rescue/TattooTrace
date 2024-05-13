from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_cors import CORS 
import os
import torch
import clip
from PIL import Image
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__, static_folder='images',)
CORS(app)  # This is to handle Cross-Origin Resource Sharing (CORS) for React interaction.

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


@app.route('/images/list')
def list_images():
    images_folder = app.static_folder
    images_list = [image for image in os.listdir(images_folder) if image.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'))]
    return jsonify(images_list)



@app.route('/analyze', methods=['POST'])
def analyze_image():
    content = request.json
    image_path = content['imagePath']
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    tattoo_prompts = [
        "A dragon tattoo symbolizes strength, wisdom, and the power to overcome challenges.",
        "A tribal tattoo represents connection to a cultural heritage, tradition, and belonging.",
        "A floral tattoo signifies beauty, the cycle of life, and new beginnings.",
        "A geometric tattoo symbolizes balance, symmetry, and the complexity of the universe.",
        "An animal tattoo often represents the traits associated with the particular animal, such as bravery for a lion.",
        "A lettering tattoo can convey specific names, messages, or quotes that hold personal significance.",
        "A portrait tattoo commemorates a loved one or idol, keeping their memory close.",
        "A skull tattoo symbolizes the acceptance of mortality and the transient nature of life.",
        "A minimalist tattoo favors simplicity and subtlety, reflecting a preference for understated beauty.",
        "A teardrop tattoo under the eye is often associated with prison time served or the loss of a loved one.",
        "Three dots tattoo, traditionally seen in a triangular formation, can mean 'mi vida loca' (my crazy life) or the cycle of life, death, and rebirth.",
        "A crown tattoo symbolizes sovereignty, control over one's life, and royal or noble essence.",
        "A spiderweb tattoo on the elbow represents being caught in the prison system, or struggle and entanglement in life's difficulties.",
        "An eight ball tattoo is often associated with risk-taking, gambling, and sometimes with drug addiction.",
        "A five-point crown tattoo is linked to royalty, excellence, and the pursuit of superiority.",
        "A gang insignia tattoo identifies affiliation with a specific gang, symbolizing loyalty and commitment.",
        "Barbed wire tattoo can signify a person's experience with imprisonment or a life of struggle and confinement.",
        "A dollar sign tattoo often represents a pursuit or love of wealth and financial success.",
        "A laughing and crying mask tattoo embodies the complexity of human emotions and the duality of happiness and sorrow.",
        "Prison bars tattoo symbolize incarceration experiences or the feeling of being trapped or confined by circumstances.",
        "A tombstone tattoo with initials commemorates a deceased person, often reflecting mourning or remembrance.",
        "A clock with no hands tattoo represents the notion that time is meaningless or an acceptance of life's unpredictability.",
        "A hand sign tattoo can indicate allegiance to a particular group or belief system, or represent specific personal or cultural messages.",
        "A rosary tattoo signifies faith, spirituality, and protection, often reflecting a deep religious commitment.",
        "A gang code number tattoo can signify affiliation with a specific gang unit or represent significant numbers within gang culture.",
        "A gang territory map tattoo marks allegiance to a gang's geographic area, symbolizing pride and territorial claims.",
        "A set of initials tattoo often commemorates a personal connection, such as family, friends, or fallen gang members.",
        "A shield and helmet tattoo represents protection, bravery, and readiness to confront life's battles.",
        "A knife or blade tattoo symbolizes survival, courage, or a warrior's spirit.",
        "Chains tattoo can represent bondage, restriction, or the overcoming of personal struggles.",
        "A neck band tattoo is often decorative but can symbolize belonging, protection, or significant life experiences.",
        "Flames tattoo symbolize transformation, passion, and the power of change.",
        "A grim reaper tattoo represents death, the end of a cycle, and sometimes the acceptance of fate.",
        "A cross on the chest tattoo signifies faith, spirituality, and guidance.",
        "Clowns faces tattoo, often showing contrasting emotions, reflect the complexity of life and the human psyche.",
        # "A gang name tattoo directly signifies loyalty to a specific gang or criminal organization.",
        "A code of silence tattoo embodies the vow of silence and loyalty within criminal organizations.",
        "An AK-47 tattoo symbolizes power, aggression, and the willingness to fight for one's beliefs or protection.",
        "A pit bull tattoo represents loyalty, strength, and often a readiness to defend.",
        "A bloods tattoo signifies affiliation with the Bloods gang, symbolizing loyalty, brotherhood, and commitment.",
        "A second dragon tattoo could emphasize the same meanings as the first or signify a particularly strong affinity or connection to the symbolism of dragons.",
        "Cat Tattoo: Signifies a thief's life, acting alone or in a gang.",
        "Star Tattoo: Each point represents a year in prison.",
        "Manacles Tattoo: Symbolizes a prison sentence of five years or longer.",
        "Epaulette Tattoo: Indicates criminal accomplishments or high-ranking criminal status.",
        "Birds on Horizon Tattoo: Represents love for freedom and escape-mindedness.",
        "Barbed Wire Tattoo: Signifies life imprisonment without parole.",
        "Cross Tattoo: Indicates bondage, subordination, or slavery.",
        "Crowns and Rings Tattoo: Shows criminal leadership or high status within penal colonies.",
        "Scarab Beetle Tattoo: A symbol of good luck for thieves, indicating a pickpocket.",
        "Swastika Tattoo: Identifies white supremacist affiliations.",
        "KKK and Noose Tattoo: Represents lynching history and Confederate flag backdrop.",
        "Neo-Nazism Tattoo: Symbolizes Invisible Empire, Knights of the Ku Klux Klan.",
        "Aryan Brotherhood Tattoo: Denotes recruitment while in prison.",
        "FAIM (Family Affiliated Irish Mafia) Tattoo: Shows affiliation with Aryan Brotherhood.",
        "Sacramaniac Tattoo: Belongs to the white supremacist group Sacramaniac.",
        "Numerical Tattoos (88, 311, 100%, 4/19, 4/20, 18, 23): Represent various supremacist and extremist beliefs.",
        "Black Guerrilla Family Tattoo: Indicates membership in a politically oriented prison gang.",
        "Red Blood Dragons Tattoo: Signifies lifelong induction into the RBD gang.",
        "Gangster Disciples Tattoo: Represents gang’s values and power to overcome oppression.",
        "Santana Tattoo: Signifies Hispanic gang membership from Orange County, California.",
        "Mexican Mafia (EME) Tattoo: Indicates powerful prison gang affiliation.",
        "Texas Syndicate (TS) Tattoo: Represents membership in the Texas Syndicate prison gang.",
        "ALKN (Almighty Latin King Nation) Tattoo: Shows allegiance to the Latin Kings gang.",
        "18th Street Gang Tattoo: Identifies membership in the 18th Street Gang.",
        "Sureños Tattoo: Represents gangs originating from Southern California.",
        "Norteños Tattoo: Signifies gangs from Northern California.",
        "Texas Chicano Brotherhood (TCB) Tattoo: Indicates membership in TCB.",
        "Mara Salvatrucha 13 (MS-13) Tattoo: Signifies MS-13 gang membership.",
        "Border Brothers Tattoo: Represents the Border Brothers prison gang.",
        "Hells Angels Tattoo: Identifies full patch members of the Hells Angels."
    ]
    tattoo_prompts += [
    "Bar Code Tattoo (Looks like victim tattoo): Linked to human trafficking in Europe, symbolizing the amount victims might have to earn for freedom.",
    "Property of... Tattoo (Looks like victim tattoo): Signifies ownership by a trafficker, often bearing the trafficker's name or nickname. Can also represent belonging to a group, though similar tattoos may exist in other contexts such as motorcycle clubs.",
    "Currency Tattoo (Looks like victim tattoo): The depiction of money, such as a money bag, coins, or dollar symbols, can represent the asking price for the trafficking victim.",
    "Neck Tattoo (Common area for victim tattoos): Often used for easily visible marks of trafficking, indicating ownership or control.",
    "Arm Tattoo (Common area for victim tattoos): May include symbols or texts signifying the victim's connection to the trafficker.",
    "Above the Groin Tattoo (Common area for victim tattoos): Placed in intimate areas to denote ownership or control, not commonly visible to the public eye."
]   
    
    clusters = {
    "Barcode": ["Bar Code Tattoo (Looks like victim tattoo): Linked to human trafficking in Europe, symbolizing the amount victims might have to earn for freedom.",
                "Property of... Tattoo (Looks like victim tattoo): Signifies ownership by a trafficker, often bearing the trafficker's name or nickname. Can also represent belonging to a group, though similar tattoos may exist in other contexts such as motorcycle clubs.",
                "Currency Tattoo (Looks like victim tattoo): The depiction of money, such as a money bag, coins, or dollar symbols, can represent the asking price for the trafficking victim.",
                ],
    "Animal": ["A dragon tattoo symbolizes strength, wisdom, and the power to overcome challenges.",
               "An animal tattoo often represents the traits associated with the particular animal such as bravery for a lion.",
               "A spiderweb tattoo on the elbow represents being caught in the prison system, or struggle and entanglement in life's difficulties.",
               "A second dragon tattoo could emphasize the same meanings as the first or signify a particularly strong affinity or connection to the symbolism of dragons.",
               "Cat Tattoo: Signifies a thief's life, acting alone or in a gang.",],
    "Regional":["A tribal tattoo represents connection to a cultural heritage, tradition, and belonging.",
                "A geometric tattoo symbolizes balance, symmetry, and the complexity of the universe."],
    "Bird": ["Birds on Horizon Tattoo: Represents love for freedom and escape-mindedness."],
    "Flower": ["A floral tattoo signifies beauty, the cycle of life, and new beginnings."],
    "Significance":["A portrait tattoo commemorates a loved one or idol, keeping their memory close.",
        "A skull tattoo symbolizes the acceptance of mortality and the transient nature of life.",
        "A minimalist tattoo favors simplicity and subtlety, reflecting a preference for understated beauty.",
        "A teardrop tattoo under the eye is often associated with prison time served or the loss of a loved one.",
        "Three dots tattoo, traditionally seen in a triangular formation, can mean 'mi vida loca' (my crazy life) or the cycle of life, death, and rebirth.",
        "A crown tattoo symbolizes sovereignty, control over one's life, and royal or noble essence.",
        "An eight ball tattoo is often associated with risk-taking, gambling, and sometimes with drug addiction.",
        "A five-point crown tattoo is linked to royalty, excellence, and the pursuit of superiority.",
        "Barbed wire tattoo can signify a person's experience with imprisonment or a life of struggle and confinement.",
        "A dollar sign tattoo often represents a pursuit or love of wealth and financial success.",
        "A laughing and crying mask tattoo embodies the complexity of human emotions and the duality of happiness and sorrow.",
        "A tombstone tattoo with initials commemorates a deceased person, often reflecting mourning or remembrance.",
        "A clock with no hands tattoo represents the notion that time is meaningless or an acceptance of life's unpredictability.",
        "A hand sign tattoo can indicate allegiance to a particular group or belief system, or represent specific personal or cultural messages.",
        "A rosary tattoo signifies faith, spirituality, and protection, often reflecting a deep religious commitment.",
        "A shield and helmet tattoo represents protection, bravery, and readiness to confront life's battles.",
        "A knife or blade tattoo symbolizes survival, courage, or a warrior's spirit.",
        "Chains tattoo can represent bondage, restriction, or the overcoming of personal struggles.",
        "A grim reaper tattoo represents death, the end of a cycle, and sometimes the acceptance of fate.",
        "A cross on the chest tattoo signifies faith, spirituality, and guidance.",
        "Clowns faces tattoo, often showing contrasting emotions, reflect the complexity of life and the human psyche.",],
    "Gang": ["A gang insignia tattoo identifies affiliation with a specific gang, symbolizing loyalty and commitment.",
              "Prison bars tattoo symbolize incarceration experiences or the feeling of being trapped or confined by circumstances.",
               "A gang code number tattoo can signify affiliation with a specific gang unit or represent significant numbers within gang culture.",
               "A gang territory map tattoo marks allegiance to a gang's geographic area, symbolizing pride and territorial claims.",
               "A set of initials tattoo often commemorates a personal connection, such as family, friends, or fallen gang members.",
               "A code of silence tattoo embodies the vow of silence and loyalty within criminal organizations.",
               "An AK-47 tattoo symbolizes power, aggression, and the willingness to fight for one's beliefs or protection.",
               "A pit bull tattoo represents loyalty, strength, and often a readiness to defend.",
               "A bloods tattoo signifies affiliation with the Bloods gang, symbolizing loyalty, brotherhood, and commitment.",
               "Star Tattoo: Each point represents a year in prison.",
               "Manacles Tattoo: Symbolizes a prison sentence of five years or longer.",
               "Epaulette Tattoo: Indicates criminal accomplishments or high-ranking criminal status.",
               "Barbed Wire Tattoo: Signifies life imprisonment without parole.",
               "Cross Tattoo: Indicates bondage, subordination, or slavery.",
               "Crowns and Rings Tattoo: Shows criminal leadership or high status within penal colonies.",
               "Scarab Beetle Tattoo: A symbol of good luck for thieves, indicating a pickpocket.",
               "Swastika Tattoo: Identifies white supremacist affiliations.",
               "Aryan Brotherhood Tattoo: Denotes recruitment while in prison.",
               "FAIM (Family Affiliated Irish Mafia) Tattoo: Shows affiliation with Aryan Brotherhood.",
               "Black Guerrilla Family Tattoo: Indicates membership in a politically oriented prison gang.",
               "Red Blood Dragons Tattoo: Signifies lifelong induction into the RBD gang.",
               "Gangster Disciples Tattoo: Represents gang’s values and power to overcome oppression.",
               "Santana Tattoo: Signifies Hispanic gang membership from Orange County, California.",
               "Mexican Mafia (EME) Tattoo: Indicates powerful prison gang affiliation.",
               "Texas Syndicate (TS) Tattoo: Represents membership in the Texas Syndicate prison gang.",
               "ALKN (Almighty Latin King Nation) Tattoo: Shows allegiance to the Latin Kings gang.",
               "18th Street Gang Tattoo: Identifies membership in the 18th Street Gang.",
               "Sureños Tattoo: Represents gangs originating from Southern California.",
               "Norteños Tattoo: Signifies gangs from Northern California.",
               "Texas Chicano Brotherhood (TCB) Tattoo: Indicates membership in TCB.",
               "Mara Salvatrucha 13 (MS-13) Tattoo: Signifies MS-13 gang membership.",
               "Border Brothers Tattoo: Represents the Border Brothers prison gang.",
               "Hells Angels Tattoo: Identifies full patch members of the Hells Angels."],
    "Neck": ["A neck band tattoo is often decorative but can symbolize belonging, protection, or significant life experiences.",
             ],
             
    "Arm": ["Arm Tattoo (Common area for victim tattoos): May include symbols or texts signifying the victim's connection to the trafficker."],
    "Others": []  # Default cluster for unmatched prompts
}

   # Analyze image and assign cluster
    max_similarity = 0
    assigned_cluster = "Others"
    for cluster, prompts in clusters.items():
        text = clip.tokenize(prompts).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)
            similarities = (image_features @ text_features.T).softmax(dim=-1)
            top_prob, top_idx = similarities[0].topk(1)
            if top_prob.item() > max_similarity:
                max_similarity = top_prob.item()
                assigned_cluster = cluster
    
    # Move image to respective folder
    destination_folder = os.path.join(app.static_folder, assigned_cluster)
    os.makedirs(destination_folder, exist_ok=True)
    shutil.move(image_path, os.path.join(destination_folder, os.path.basename(image_path)))
    


    return jsonify({
        "cluster": assigned_cluster,
        "confidence": max_similarity
    })

if __name__ == '__main__':
    app.run(debug=True)