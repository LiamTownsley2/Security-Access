from Util import generate_unique_id
from ..db import users_table, thread_logger

def register_user(name: str):
    user_id = generate_unique_id()
    users_table.put_item(
        Item={
            "UserID": user_id,
            "Name": name,
        }
    )
    return user_id

def delete_user(user_id: str):
    response = users_table.delete_item(
        Key={"UserID": user_id}
    )
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200

def get_user(user_id: str):
    thread_logger.info(f"Attempting to retrieve user with UserID: {user_id}")
    response = users_table.get_item(Key={"UserID": user_id})
    thread_logger.info(f"Get_User RESPONSE ->>>> {response.get('Item')}")
    return response.get('Item')

def get_all_users():
    thread_logger.info("Attempting to retrieve all users.")
    response = users_table.scan()
    thread_logger.info(f"Get_All_Users RESPONSE ->>>> {response.get('Items')}")
    return response.get('Items')

def edit_user(user_id: str, name: str = None, card_id: str = None, last_scanned: str = None):
    existing_user = get_user(user_id)
    if not existing_user:
        thread_logger.warning(f"User with UserID: {user_id} not found.")
        return None
    
    update_expression = "set"
    expression_values = {}
    
    if name:
        update_expression += " Name = :name,"
        expression_values[":name"] = name
    
    if card_id:
        update_expression += " CardID = :card_id,"
        expression_values[":card_id"] = card_id
    
    if last_scanned:
        update_expression += " LastScanned = :last_scanned,"
        expression_values[":last_scanned"] = last_scanned
    
    update_expression = update_expression.rstrip(",")
    if not expression_values:
        thread_logger.warning("No fields to update.")
        return None
    
    response = users_table.update_item(
            Key={"UserID": user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW"
        )
    
    updated_item = response.get("Attributes")
    thread_logger.info(f"Edit_User RESPONSE ->>>> {updated_item}")
    return updated_item