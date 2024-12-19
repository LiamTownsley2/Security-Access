from ..db import dynamodb

users_table = dynamodb.Table("Users")
access_log_table = dynamodb.Table("AccessLog")