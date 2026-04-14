from werkzeug.security import generate_password_hash, check_password_hash

pass1 = "pa3453454"
has_pass_1 = generate_password_hash(pass1)
pass2 = "pa3453454"

print(check_password_hash(has_pass_1, pass2))

