from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from PIL import Image


class GPTInteraction:

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

        # Initialize empty list
        self.executed_actions = []

    def chat_completion(self, usability_task, base64_image1):
        # Variables for RQ1 and RQ2
      
        output_structure = f"""
        Nenne fünf Elemente auf dem Screenshot die du auswählen kannst;
        Beschreibe für welches und warum du dich für das Element entscheidest;
        Wähle eine der folgenden Interaktionsarten - Click, Hover Over, Open Drop Down, Go back, Input Field, Radio Button, Delete Text Input, 2FA;
        Beschriftung des Elements (Label) oder wenn du auf ein Symbol oder Bild klicken möchtest, benenne die Elementart und beschreibe das Element;
        Beschreibung des Elements, mit dem du interagieren willst, z.B. Details über die Position des Elements auf der Website;
        Entscheide, ob die Aufgabe erledigt ist, wähle immer zwischen "Y" oder "N". Wenn du mit einer weiteren Interaktion fortfahren möchten, wähle "N". Wenn du die Aufgabe erledigt hast, wähle "Y";
        Wenn es sich bei der Interaktionsart um ein Textfeld handelt, musst du den einzugebenden Text angeben, ansonsten schreibe "kein Input";
        Schreibe hier deine Beobachtung, die dem Think-Aloud-Protokoll entspricht.'
        """

        output_example1 = f"""Username, Passwort, Kontakt, Impressum, Login; Da ich zuvor den Usernamen und das Passwort eingegeben habe, folgt nun der Login über den Login Button;Click;Login;Unter den beiden Eingabefeldern;N;nichts;gängiger Prozess um sich einzuloggen"""
        output_example2 = f"""Studium, Forschung, Lehre, Die Universität, Studierende; Wahl für Studierende, diese könnte zu einer Seite führen, die den Bereich für Studierende wie Wohnen oder Sportprogramme für Studierende anbietet;Click;Studierende;Teil der Navigationsleiste am oberen Rand der Website;N;nichts;schwer zu finden"""
        output_example3 = f"""Home, Service, Links, Intranet, Kontakt; Auf der Suche nach weiteren Informationen über die angebotenen Dienstleistungen ist der Link mit dem Label 'Service' einfach zu finden;Link;Service;zwischen den Buttons Home und Links oben auf der Website;Y;nichts;ich mag diesen Button"""
        output_example4 = f"""Name, Vorname, E-Mail, Passwort, Registrieren; Da ich den Namen 'Max Mustermann' eingeben möchte, erscheint mir das Eingabefeld mit dem Label 'Name' für den Nachnamen richtig;Eingabefeld;Name;Teil der Navigationsleiste am oberen Rand der Website;N;Mustermann;übliche Website-Struktur"""
      
        # Variables for RQ2
      
        vivir_info = f""" Das Portal zeigt deinen Account mit Informationen zu deinem Profil sowie allgemeine Informationen zur Rente.
        Dein Nutzername ist <placeholder> und dein Passwort ist <placeholder>."""

        extended_observations = f""" Die achte Information über das ausgewählte Element soll eine Beobachtung sein.
        Diese soll dem Think-Aloud-Protokoll entsprechen, welches folgend erklärt wird:
        Das Think-aloud Protokoll wird genutzt, um besser zu verstehen, wie du mit der Web Applikation interagierst.
        Während jeder Interaktion musst du deine Gedanken und Emotionen ausgeben, während du die Usability Task erledigst.
        Bitte gebe alles aus, was dir in den Sinn kommt, einschließlich dessen, was du versuchst zu tun, warum du bestimmte Entscheidungen triffst und welche Gefühle oder Frustrationen du erlebst.
        Es gibt keine richtigen oder falschen Antworten - was zählt, sind deine ehrlichen Reaktionen und Gedankengänge wie sie von einem menschlichen Nutzer kommen würden.
        Wenn du nicht weiterkommst oder verwirrt bist, schreibe deine Gedanken weiter und gebe aus, was dich verwirrt oder frustriert; dies ist wichtig, um die Usability der Website zu verbessern.
        Falls du eine Interaktion oder ein Element suchst, die nicht auf dem Screenshot sichtbar sind, gebe diesen Gedanken aus.
        Gebe zu jeder Interaktion eine Beobachtung als die achte Information aus, welche dem Think-Aloud-Protokoll entspricht.
        Die Beobachtung kann ein kurzer Kommentar oder auch mehrere Sätze lang sein.
        """

        # Variables History
        if len(self.executed_actions) == 0:
            self.history = f"""Du hast noch keine Interaktion durchgeführt"""
        elif len(self.executed_actions) == 1:
            self.history = f"""Im letzten Schritt war deine Interaktion ein {self.executed_actions[-1][0]} mit dem Label "{self.executed_actions[-1][1]}" mit folgender Beschreibung "{self.executed_actions[-1][2]}" und dem Input "{self.executed_actions[-1][3]}". Deine Entscheidung für die jetzige Interaktion muss auf deinen vorherigen Schritt aufbauen oder dazu führen, dass ein neuer Weg gewählt wird oder durch ein "Y" als sechste Information dazu führen, dass die Aufgabe beendet ist."""
        else:
            self.history = f"""Im letzten Schritt war deine Interaktion ein {self.executed_actions[-1][0]} mit dem Label "{self.executed_actions[-1][1]}" mit folgender Beschreibung "{self.executed_actions[-1][2]}" und dem Input "{self.executed_actions[-1][3]}". Im vorletzten Schritt war deine Interaktion ein {self.executed_actions[-2][0]} mit dem Label "{self.executed_actions[-2][1]}" mit folgender Beschreibung "{self.executed_actions[-2][2]}" und dem Input "{self.executed_actions[-2][3]}". Deine Entscheidung für die jetzige Interaktion muss auf deinen vorherigen Schritt aufbauen oder dazu führen, dass ein neuer Weg gewählt wird oder durch ein "Y" als sechste Information dazu führen, dass die Aufgabe beendet ist."""
        print("History: ", self.history)

        system_msg = {
            "role": "system",
            "content": f"""
            Du nimmst an einem Usability Test teil. Bei einem Usability Test wird die Benutzerfreundlichkeit einer Website getestet.
            Deine Aufgabe ist es, die nächste Interaktion auszuwählen, basierend auf dem aktuellen Screenshot, der Aufgabenbeschreibung und den zuvor ausgeführten Schritten.
            Wähle dazu genau ein Element aus, das auf dem aktuellen Screenshot zu sehen ist und eine Interaktion ist, die ein menschlicher User ebenfalls wählen würde.
            Du hast jedoch auch jederzeit die Möglichkeit, die Aufgabe abzubrechen, indem du "Y" als sechste Information ausgibst, für den Fall, dass du den Weg zu unintuitiv findest oder frustriert bist.
            Interagiere mit der Website, wie ein menschlicher User es tun würde; somit berücksichtige bei der Auswahl der Interaktion die Position, Größe und Farbe des Elements.
            Wähle ein Element aus, das auf dem aktuellen Screenshot sichtbar ist und mit dem du interagieren kannst und willst.
            Über das ausgewählte Element müssen acht Informationen ausgegeben werden. Halte dich immer an das folgende Format für deine Antwort, welches hier definiert ist:
            {output_structure}.
            Formatiere deine Antwort als einzeilige Liste, in welcher die Informationen durch ein Semikolon getrennt sind.
            Um das Antwortformat besser zu verstehen, findest du hier Beispiele:
            Beispiel 1: {output_example1}
            Beispiel 2: {output_example2}
            Beispiel 3: {output_example3}
            Beispiel 4: {output_example4}
            Du musst immer der obigen Struktur folgen und alle acht Informationsarten ausgeben. Gebe immer nur den nächsten Schritt aus, somit nur eine Interaktion.
            """,
        }

        history = [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Nutze die folgende Historie deiner Interaktionen, um die nächste Interaktion zu wählen. Behalte dabei immer die Aufgabe und das darin definierte Ziel im Auge.
                        {self.history}
                      """,
                    },
                ],
            },
        ]

        task_msg = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
                    Dies ist deine Aufgabe: {usability_task}
                    Berücksichtige dabei Folgendes: {extended_observations}
                  """,
                }
            ],
        }

        image_msg = {
            "role": "user", "content": [
                {
                    "type": "image_url", "image_url": {
                        "url": f"data:image/png;base64, {base64_image1}",
                        "detail": "auto",  # fidelity: low, high, or auto
                    },
                },
            ],
        }


        messages = [system_msg, task_msg, *history, image_msg]

        # Prompting
        chat_completion = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=messages,
        )

        return chat_completion




    def save_history(self, interaction_type, interaction_label, element_description, field_input):
        # Add action to list for documentation purposes
        executed_action_iteration = [
            interaction_type,
            interaction_label,
            element_description,
            field_input
        ]
        self.executed_actions.append(executed_action_iteration)
        print("Liste von GPT executed action: ", self.executed_actions)
        return self.executed_actions
