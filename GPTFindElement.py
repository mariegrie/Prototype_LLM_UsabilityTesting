from dotenv import load_dotenv
import os
from openai import AzureOpenAI

class GPTFindElement:

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Create client
        client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("OPENAI_API_URL"),
        )

        # Client initialization
        self.client = client

    def chat_completion(self, current_html_code, last_gpt_interaction):
        # Variables for Prompting
        task = f"""
        Du erhältst eine Beschreibung eines Web-Elements und den HTML-Code der dazugehörigen Website. Suche das beschriebene Element im HTML-Code. Wähle basierend auf der Beschreibung das Element aus, falls mehrere Elemente der Beschreibung entsprechen, wähle das Element, mit dem ein menschlicher User am wahrscheinlichsten interagieren würde.
        Gebe die Informationen in der Reihenfolge aus, wie sie in der Ausgabestruktur beschrieben sind, und gebe sie in einer Zeile und durch ein Semikolon getrennt aus.
        Halte dich strikt an das in der Ausgabestruktur und den Beispielen definierte Ausgabeformat.
        Der CSS-Selektor muss eindeutig und präzise sein. Es ist sehr wichtig, dass der CSS-Locator nur auf ein Element verweist und als Locator für Selenium im Firefox-Browser funktioniert.
        """

        output_structure = f"""Gebe eine kurze Erklärung, warum du dieses Element ausgewählt hast und wie der CSS-Selektor erstellt werden soll;Typ des Elements;Label des Elements;HTML-Tag des Elements;Element-ID, nur wenn es keine ID gibt, gebe „no id“ aus;Erstelle den CSS-Selektor des Elements, nur wenn dies nicht möglich ist, gebe „no css“ aus. Halte dich strikt an die CSS-Struktur und das Format. Stelle sicher, dass der CSS-Selektor präzise ist und das Element eindeutig identifiziert wird; er darf nur auf ein einziges Element im HTML-Code verweisen;href des Elements, nur wenn es keinen href gibt, gebe „no href“ aus;Element class, wenn es eine class gibt, andernfalls gebe „no class“ aus;gebe das gesamte Element aus 
         """

        output_example1 = f"""Das Element enthält die in der Eingabe definierte Label und ist Teil der Hauptnavigationsleiste, daher beginnt der CSS-Selektor mit dem Hashtag #main;Button;Intranet;<a>;no id;#zielgruppennavigation > li:nth-child(6) > a;/de/intern/index.shtml;nav-item-audience;<li class="nav-item-audience"><a href="/de/intern/index.shtml">Intranet</a></li>"""
        output_example2 = f"""Der Selektor des Elements ist nur ein Hashtag, weil dieser ausreicht, um es als eindeutiges Element zu lokalisieren; Drop Down Menu; Wettkampf;<a>;sm-17189653389772473-1;#sm-17195621891684329-1;https://www.sparda-muenster-city-triathlon.de/wettkampf/;elementor-item has-submenu;<a href="https://www.sparda-muenster-city-triathlon.de/wettkampf/" class="elementor-item has-submenu" id="sm-17189653389772473-1" aria-haspopup="true" aria-controls="sm-17189653389772473-2" aria-expanded="false">Wettkampf<span class="sub-arrow"><i class="fas fa-caret-down"></i></span></a> """
        output_example3 = f"""Das Element wird anhand der Bezeichnung „Name“ und seiner Position unter dem Abschnitt „Kontakt“ identifiziert. Der CSS-Selektor ist so aufgebaut, dass er dieses Eingabefeld innerhalb des Formulars eindeutig identifiziert;input field;Name;<input>;no id;#eael-ninja-form-5393 #nf-field-1;no href;no class;<input type="text" value="" class="nf-element" id="nf-field-1" name="nf-field-1-textbox" aria-invalid="false" aria-describedby="nf-error-1" aria-labelledby="nf-label-field-1" required=""> """
        output_example4 = f"""Das Element wird anhand der Bezeichnung „Nutzerkennung“ und seiner Position als oberstes Eingabefeld im Anmeldeformular identifiziert;input field;Name;<input>;no id;#mat-input-36;no href;no class;<input _ngcontent-one-c275="" matinput="" type="text" formcontrolname="username" class="mat-input-element mat-form-field-autofill-control ng-tns-c113-61 ng-pristine ng-invalid cdk-text-field-autofill-monitored ng-touched" required="" id="mat-input-36" aria-required="true" aria-describedby="mat-error-4"> """
        output_example5 = f"""Das Element ist Teil der Liste Links der Website und befindet sich an vierter Stelle;Button;Organisation;<a>;no id;ul.linkliste:nth-child(1) > li:nth-child(4) > a:nth-child(1);/studium/orga/index.html;class="int";<a href="/studium/orga/index.html" class="int" hreflang="">Organisation</a>"""
                        
        element_description = f"""Das Element hat das Label {last_gpt_interaction[1]} und die Interaktion ist ein {last_gpt_interaction[0]}. Dabei kann die Interaktion "Click" bedeuten, dass es ein Button, Link, Icon oder auch Bild ist. Es befindet sich an folgender Stelle der Website "{last_gpt_interaction[2]}"."""

        system_msg = {
            "role": "system",
            "content": f"""
            Du bist ein Experte für CSS-Locator. Anhand einer Beschreibung eines Elements und des HTML-Codes der Seite kannst du ein Element identifizieren und Informationen darüber ausgeben, insbesondere einen eindeutigen CSS-Locator.
            Der CSS-Selektor muss derselbe sein, den ich als 'Copy CSS Selector' mit der Untersuchen-Funktion im Firefox-Browser exportieren kann.
            Es ist extrem wichtig, dass der CSS-Locator korrekt ist und das richtige Element lokalisiert.
            Du musst immer neun Informationen ausgeben. Gebe nie weniger oder mehr als die neun Informationen aus.
            Du musst die Antwort immer in folgendem Format ausgeben: {output_structure}.
            Gebe hierbei nur die Information aus und nicht die Beschreibung der Information.
            Um das Ausgabeformat zu verdeutlichen, findest du hier Beispiele:
            Beispiel 1: {output_example5}
            Beispiel 2: {output_example2}
            Beispiel 3: {output_example3}
            Beispiel 4: {output_example4}
            Beispiel 5: {output_example1}
            Du musst dich immer an das Format halten und die Ausgabe im gleichen Format vornehmen. Gebe immer alle neun Informationen wie in der Aufgabe beschrieben aus. Der CSS-Selektor, der die sechste Information darstellt, muss eindeutig und präzise sein. Es ist sehr wichtig, dass er nur auf ein Element im HTML-Code verweist.
            """,
        }

        task_msg = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
                    {task}
                    Beschreibung des gesuchten Elements: {element_description}
                    Zur Erstellung des Locators nutze den HTML-Code, der das beschriebene Element enthält: {current_html_code}
                    """,
                }
            ],
        }

        messages = [system_msg, task_msg]

        # Prompting
        chat_completion = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            # frequency_penalty=0.5,
            messages=messages,
        )

        # Tokens for Prompting (differs from chat completion output)
        self.count_tokens = [system_msg, task_msg]

        return chat_completion

