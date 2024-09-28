package contactProject;

/**
 * Instance of a contact entry to allow user to store contact's name, phone number, and email.
 * @author Yiming Lian
 */
public class Contact {
  private String name;
  private String phoneNumber;
  private String email;

  /**
   * Constructs a new Contact object with the specified name, phone number, and email address
   * @param name
   * @param phoneNumber
   * @param email
   */
  public Contact(String name, String phoneNumber, String email) {
    this.name = name;
    this.phoneNumber = phoneNumber;
    this.email = email;
  }

  /**
   * This method return the contact's name
   * @return contact's name
   */
  public String getName() {
    return name;
  }
  
  /**
   * This method return the contact's phone number
   * @return contact's phone number
   */
  public String getPhoneNumber() {
    return phoneNumber;
  }
  
  /**
   * This method return the contact's email
   * @return contact's email
   */
  public String getEmail() {
    return email;
  }

  /**
   * This method set the contact's name
   * @param name
   */
  public void setName(String name) {
    this.name = name;
  }
  
  /**
   * This method set the contact's phone number
   * @param phoneNumber
   */
  public void setPhoneNumber(String phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  /**
   * This method set the contact's email
   * @param email
   */
  public void setEmail(String email) {
    this.email = email;
  }

  /**
   * This method print the contact's name, phone number, and email
   */
  @Override
  public String toString() {
    return "Name: " + name + "\nPhone Number: " + phoneNumber + "\nEmail: " + email;
  }
  
  /**
   * This method convert contact object into text format
   * @return string of the contact information
   */
  public String toTxtFormat() {
    return name + "," + phoneNumber + "," + email + "\n";
  }
  

}
