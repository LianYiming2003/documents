package contactProject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class tester {
  static String list = "";
  static String originalList = "";
  
  public static boolean test1() {
    try {
      File txtFile = new File(ContactManager.getFileName());
      FileReader fileReader = new FileReader(txtFile);
      BufferedReader bufferReader = new BufferedReader(fileReader);
      
      String line = bufferReader.readLine();
      while(line != null) {
        Contact contact = ContactManager.toContactFormat(line);
        list += contact + "\n---------------------------\n";
        originalList += line + "\n";
        line = bufferReader.readLine();
      }
      bufferReader.close();
    }catch(IOException e) {
      System.out.println(e);
    }
    //System.out.println(list);
    String results = ContactManager.viewAllContacts();
    //System.out.println(results);
    if (list.length() == 0) {
      if (results.equals("No contacts available.")) {
        System.out.println("1)viewAllContacts method pass");
        return true;
      }
    }else {
      if (list.equals(results)) {
        System.out.println("1)viewAllContacts method pass");
        return true;
      }
    }
    System.out.println("1)viewAllContacts method fail");
    return false;
  }
  
  public static boolean test2() {
    list = "";
    Contact testContact = new Contact("Alice", "123456789", "alice@example.com");
    ContactManager.addContact(testContact);
    ContactManager.writeFile();
    String results = ContactManager.viewAllContacts();
    try {
      File txtFile = new File(ContactManager.getFileName());
      FileReader fileReader = new FileReader(txtFile);
      BufferedReader bufferReader = new BufferedReader(fileReader);
      
      String line = bufferReader.readLine();
      while(line != null) {
        Contact contact = ContactManager.toContactFormat(line);
        list += contact + "\n---------------------------\n";
        line = bufferReader.readLine();
      }
      bufferReader.close();
    }catch(IOException e) {
      System.out.println(e);
    }
    //System.out.println(results);
    //System.out.println(list);
    if (list.equals(results)) {
      System.out.println("2)addContact method pass");
      return true;
    }
    System.out.println("2)addContact method fail");
    
    return false;
  }
  
  public static boolean test3() {
    String results = ContactManager.searchContactByName("Alice");
    String info = "Name: " + "Alice" + "\nPhone Number: " + "123456789" + "\nEmail: " + "alice@example.com" + "\n---------------------------";
    //System.out.println(results);
    //System.out.println(Info);
    if (results.equals(info)) {
      System.out.println("3)searchContactByName method pass");
      return true;
    }
    System.out.println("3)searchContactByName method fail");
    return false;
  }
  
  public static boolean test4() {
    list = "";
    ContactManager.deleteContactByName("Alice");
    ContactManager.writeFile();
    try {
      File txtFile = new File(ContactManager.getFileName());
      FileReader fileReader = new FileReader(txtFile);
      BufferedReader bufferReader = new BufferedReader(fileReader);
      
      String line = bufferReader.readLine();
      while(line != null) {
        list += line + "\n";
        line = bufferReader.readLine();
      }
      bufferReader.close();
    }catch(IOException e) {
      System.out.println(e);
    }
    //System.out.println(list);
    //System.out.println(originalList);
    if (list.equals(originalList)) {
      String results = ContactManager.deleteContactByName("Alice");
      if (results.equals("Contact not found.")) {
        System.out.println("4)deleteContactByName method pass");
        return true;
      }
    }
    System.out.println("4)deleteContactByName method fail");
    return false;
  }
  
  public static void resetDatabase() {
    try {
      File txtFile = new File(ContactManager.getFileName());
      FileWriter fileReader = new FileWriter(txtFile);
      BufferedWriter bufferWriter = new BufferedWriter(fileReader);
      
      bufferWriter.append(originalList);
      bufferWriter.close();
    }catch(IOException e) {
      System.out.println(e);
    }
  }

  public static void main(String[] args) {
    // TODO Auto-generated method stub
    ContactManager.readFile();
    test1();
    test2();
    test3();
    test4();
    resetDatabase();
    //ContactManager.writeFile();
  }

}
