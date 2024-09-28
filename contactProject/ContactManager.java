package contactProject;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;
import java.io.*;

/**
 * This class provides functionality for managing a list of contacts.
 * @author Yiming Lian
 */
public class ContactManager {

  private static ArrayList<Contact> contactList = new ArrayList<>();
  private static final String FILE_NAME = "contacts.txt";
  
  /**
   * This file will return the database's name to the tester method to check the function.
   * @return database's name
   */
  public static String getFileName() {
    return FILE_NAME;
  }
  
  /**
   * This method convert text format into contact object
   * @param line of contact information
   * @return contact object store contact information
   */
  public static Contact toContactFormat(String line) {
    String[] arrOfLine = line.split(",");
    return new Contact(arrOfLine[0], arrOfLine[1], arrOfLine[2]);
  }
  
  /**
   * This method read the text file into the program
   */
  public static void readFile() {
    try {
      File txtFile = new File(FILE_NAME);
      FileReader fileReader = new FileReader(txtFile);
      BufferedReader bufferReader = new BufferedReader(fileReader);
      
      String line = bufferReader.readLine();
      while(line != null) {
        Contact contact = toContactFormat(line);
        contactList.add(contact);
        line = bufferReader.readLine();
      }
      bufferReader.close();
    }catch(IOException e) {
      System.out.println(e);
    }
  }
  
  /**
   * This method write the information to the text file
   */
  public static void writeFile() {
    try {
      File txtFile = new File(FILE_NAME);
      FileWriter fileReader = new FileWriter(txtFile);
      BufferedWriter bufferWriter = new BufferedWriter(fileReader);
      
      for(int i = 0; i < contactList.size(); i++) {
        bufferWriter.append(contactList.get(i).toTxtFormat());
      }
      bufferWriter.close();
    }catch(IOException e) {
      System.out.println(e);
    }
  }
  
  /**
   * This method add a new contact
   * @param contact
   */
  public static void addContact(Contact contact) {
    contactList.add(contact);
    System.out.println("Contact added successfully!");
  }

  /**
   * This method shows whole contacts
   */
  public static String viewAllContacts() {
    String result = "";
    // if the list is null, show no contacts
    if (contactList.isEmpty()) {
      result ="No contacts available.";
    } else {
      for (Contact contact : contactList) {
        result += contact + "\n";
        result += "---------------------------\n";
      }
    }
    return result;
  }

  /**
   * This method using name that user input to search other information
   * @param name
   */
  public static String searchContactByName(String name) {
    String result = "";
    boolean found = false;
    for (Contact contact : contactList) {
      //Using toLowerCase method to perform a case-insensitive comparison
      if (contact.getName().toLowerCase().equals(name.toLowerCase())) {
        found = true;
        result += contact + "\n---------------------------";
      }
    }
    if (!found) {
      result = "Contact not found.";
    }
    return result;
  }
  
  /**
   * This method using name that user input to delete information
   * @param name
   */
  public static String deleteContactByName(String name) {
    String result = "";
    boolean found = false;
    Iterator<Contact> iterator = contactList.iterator();//Except ConcurrentModificationException
    while (iterator.hasNext()) {
        Contact contact = iterator.next();
        if (contact.getName().toLowerCase().equals(name.toLowerCase())) {
            iterator.remove();
            result = "Contact deleted successfully!";
            found = true;
        }
    }
    if (!found) {
      result = "Contact not found.";
    }
    return result;
  }

  public static void main(String[] args) {
    readFile();
    Scanner sc = new Scanner(System.in);
    boolean con = true;
    while (con) { // only exit when user press 5
      String userChoice;
      System.out.println();
      System.out.println("You are in the Main Menu:\n" + "\t 1) Add Contact\n"
          + "\t 2) View All Contacts\n" + "\t 3) Search Contact by Name\n"
          + "\t 4) Delete Contact by Name\n" + "\t 5) Exit\n");
      userChoice = sc.nextLine();
      userChoice = userChoice.trim(); // Remove any leading or trailing whitespace
      switch (userChoice) {
        case "1":
          System.out.print("Enter name: ");
          String name = sc.nextLine();
          System.out.print("Enter phone number: ");
          String phoneNumber = sc.nextLine();
          System.out.print("Enter email: ");
          String email = sc.nextLine();
          Contact contact = new Contact(name, phoneNumber, email);
          addContact(contact);
          break;
        case "2":
          System.out.println(viewAllContacts());
          break;
        case "3":
          System.out.print("Enter name to search: ");
          String searchName = sc.nextLine();
          System.out.println(searchContactByName(searchName));
          break;
        case "4":
          System.out.print("Enter name to delete: ");
          String deleteName = sc.nextLine();
          System.out.println(deleteContactByName(deleteName));
          //System.out.print("1");
          break;
        case "5":
          System.out.println("Exiting...");
          con = false;
          sc.close();
          break;
        default:
          System.out.print("Invalid input, please try again.");
      }
    }
    writeFile();
  }

}
