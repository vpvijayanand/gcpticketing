import mariadb
import pandas as pd

class TicketCreation:
    def __init__(self):
        """Initialize the MySQL connection."""
        try:
            self.connection = mariadb.connect(
                host="localhost",
                database="ticket_db",
                user="ticketadmin",
                password="Ticket@123"
            )
            if self.connection:
                print("Connected to MariaDB database")
        except Exception as e:
            print(f"Error while connecting to MariaDB: {e}")
            self.connection = None

    def fetch_language_data(self, language):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = f"SELECT DISTINCT a.id FROM agent_language_mapping am INNER JOIN Agents a ON a.id = am.agent_id WHERE language = '{language}'"
                return pd.read_sql(query, self.connection)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

    def fetch_category_data(self, category):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = f"SELECT DISTINCT a.id FROM agent_category_mapping am INNER JOIN Agents a ON a.id = am.agent_id WHERE category = '{category}'"
                return pd.read_sql(query, self.connection)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

    def create_ticket(self, original_text, language, category, severity):
        """Insert ticket details into the database."""
        if self.connection:
            try:
                df_language = self.fetch_language_data(language)
                df_category = self.fetch_category_data(category)

                # Join the DataFrames to find an agent who knows both the language and category
                df_joined = pd.merge(df_language, df_category, on='id', how='inner')
                agent_list = df_joined['id'].tolist()

                if agent_list:
                    agent_id = agent_list[0]
                    cursor = self.connection.cursor()
                    query = f"""
                    INSERT INTO ticket_details 
                    (problem_description, language, category, severity, assigned_agent_id, ticket_status)
                    VALUES ('{original_text}', '{language}', '{category}', '{severity}', {agent_id}, 'Open');
                    """
                    cursor.execute(query)
                    self.connection.commit()
                    print(f"Ticket created and assigned to agent ID: {agent_id}")
                else:
                    print("No agent found with the required language and category.")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

    def close_connection(self):
        """Close the MariaDB connection."""
        if self.connection:
            self.connection.close()
            print("MariaDB connection is closed")
