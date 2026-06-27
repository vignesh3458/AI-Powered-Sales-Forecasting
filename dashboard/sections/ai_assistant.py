import streamlit as st


from ai_engine.llm_assistant import ask_lucid_ai





def show_ai_assistant(df):


    st.title(
        "🤖 AURA AI Business Assistant"
    )


    st.caption(
        """
Ask AURA about:
• Revenue performance
• Sales trends
• Forecast insights
• Customer behaviour
• Business strategy
"""
    )





    # ==========================
    # CHAT MEMORY
    # ==========================


    if "aura_messages" not in st.session_state:


        st.session_state.aura_messages = [

            {

                "role":"assistant",

                "content":
                """
Hello 👋  
I am AURA AI.

I can analyze:
📈 Revenue  
🔮 Forecasting  
🍽 Products  
👥 Customers  
💰 Business Growth  

Ask me anything.
"""

            }

        ]






    # ==========================
    # DISPLAY HISTORY
    # ==========================


    for message in st.session_state.aura_messages:


        with st.chat_message(

            message["role"]

        ):


            st.markdown(

                message["content"]

            )







    # ==========================
    # USER QUESTION
    # ==========================


    question = st.chat_input(

        "Ask AURA AI..."

    )





    if question:



        st.session_state.aura_messages.append(

            {

                "role":"user",

                "content":question

            }

        )






        with st.chat_message(

            "user"

        ):


            st.markdown(

                question

            )








        # ==========================
        # AI RESPONSE
        # ==========================


        with st.chat_message(

            "assistant"

        ):



            with st.spinner(

                "Analyzing restaurant intelligence..."

            ):



                try:


                    answer = ask_lucid_ai(

                        question,

                        df

                    )



                except Exception as e:



                    answer = (

                        "⚠️ AURA AI connection failed.\n\n"

                        "Check Ollama server is running."

                    )






                st.markdown(

                    answer

                )







        st.session_state.aura_messages.append(

            {

                "role":"assistant",

                "content":answer

            }

        )