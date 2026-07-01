import os
import sys
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("Error: Falta configurar GROQ_API_KEY en el archivo .env")
    print("Por favor, obtén tu API key gratuita en https://console.groq.com y agrégala a .env")
    sys.exit(1)

def get_weather(city: str) -> str:
    return f"El clima simulado en {city} es soleado."

def buscar_informacion_empresa(tema: str) -> str:
    tema_minusculas = tema.lower()
    
    base_conocimiento = {
        "horarios": "Nuestro horario de atención es de Lunes a Viernes de 9:00 AM a 6:00 PM.",
        "soporte": "Para soporte técnico, escribe un correo a soporte@empresa.com.",
        "ventas": "Para ayuda con una cotización, contacta a ventas@empresa.com.",
        "recursos humanos": "Recursos Humanos se encarga de contratación, nóminas y bienestar de los empleados.",
        "contraseña": "Para recuperar tu contraseña, ve a la web y haz clic en 'Olvidé mi contraseña'.",
        "facturación": "Para solicitar una factura, envía tu ticket a facturas@empresa.com."
    }
    
    for clave, respuesta in base_conocimiento.items():
        if clave in tema_minusculas:
            return respuesta
            
    return "No encontré información sobre ese tema."

lista_herramientas = [get_weather, buscar_informacion_empresa]

modelo_nombre = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
llm = ChatGroq(model=modelo_nombre)

def formatear_pregunta(pregunta_usuario: str) -> str:
    return f"Por favor responde a esta consulta del usuario: {pregunta_usuario}"

chain_basica = RunnableLambda(formatear_pregunta)

agente = create_agent(
    model=llm,
    tools=lista_herramientas,
    system_prompt="Eres un asistente amigable. Usa tus herramientas para responder las preguntas del usuario."
)

memoria = []

def main():
    while True:

        print("AGENTE BÁSICO CON LANGCHAIN")

        print("1. Preguntar al agente")
        print("2. Ver memoria de conversación")
        print("3. Salir")
        print("=====================================")
        
        opcion = input("Elige una opción (1-3): ")
        
        if opcion == "1":
            pregunta = input("\nEscribe tu pregunta: ")
            
            print("\nProcesando...")
            try:
                pregunta_procesada = chain_basica.invoke(pregunta)
                
                resultado = agente.invoke(
                    {"messages": [{"role": "user", "content": pregunta_procesada}]}
                )
                
                mensaje_final = resultado["messages"][-1]
                
                if hasattr(mensaje_final, 'content') and isinstance(mensaje_final.content, str):
                    respuesta_agente = mensaje_final.content
                elif hasattr(mensaje_final, 'content') and isinstance(mensaje_final.content, list):
                    respuesta_agente = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in mensaje_final.content)
                else:
                    respuesta_agente = str(mensaje_final.content)
                
                print(f"\nRespuesta: {respuesta_agente}")
                
                memoria.append({
                    "pregunta": pregunta,
                    "respuesta": respuesta_agente
                })
            except Exception as e:
                print(f"\nHubo un error de conexión o ejecución: {e}")
                
        elif opcion == "2":
            print("\nMEMORIA DE CONVERSACION")
            if len(memoria) == 0:
                print("La memoria está vacía.")
            else:
                for idx, item in enumerate(memoria, 1):
                    print(f"\n[{idx}] Pregunta: {item['pregunta']}")
                    print(f"    Respuesta: {item['respuesta']}")

            
        elif opcion == "3":
            print("\nSaliendo del programa... ¡Hasta pronto!")
            break
        else:
            print("\nOpción incorrecta. Intenta de nuevo.")

if __name__ == "__main__":
    main()
