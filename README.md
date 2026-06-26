# S2-D4 — LangChain: chains, agents y tools básicas

Este proyecto demuestra de forma básica cómo un agente puede usar herramientas externas y una memoria simple para responder preguntas del usuario desde consola.

## ¿Qué hace este proyecto?

Es una aplicación de consola en Python que permite interactuar con un asistente de inteligencia artificial (Agente). El asistente es capaz de usar herramientas (Tools) para obtener información que no conoce de forma nativa, como el clima de una ciudad o información interna de una empresa.

## Conceptos clave de LangChain utilizados

- **Chain (Cadena):** Una cadena es una secuencia de llamadas a componentes (como modelos, transformaciones de texto, etc.). En este proyecto se incluye una chain básica para formatear la pregunta del usuario antes de enviarla al agente.
- **Agent (Agente):** Es el sistema que utiliza un modelo de lenguaje (LLM) como motor de razonamiento para decidir qué acciones tomar y qué herramientas utilizar para responder a una pregunta.
- **Tool (Herramienta):** Funciones o habilidades que le damos al agente para interactuar con el mundo exterior. Aquí usamos dos: una para consultar el clima y otra para buscar en una base de conocimientos simulada.
- **Memoria Básica:** Un mecanismo para recordar interacciones pasadas. En este proyecto se utiliza una lista simple en Python que guarda el historial de la conversación actual.
