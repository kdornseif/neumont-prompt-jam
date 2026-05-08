def collect_contact():
    """Collect one contact record from user input."""
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone number: ").strip()

    return {
        "name": name,
        "email": email,
        "phone": phone
    }


contacts = []

while True:
    contact = collect_contact()
    contacts.append(contact)

    another = input("Add another contact? (y/n): ").strip().lower()
    if another != "y":
        break

print("\nSaved contacts:")
for contact in contacts:
    print(f"{contact['name']} | {contact['email']} | {contact['phone']}")