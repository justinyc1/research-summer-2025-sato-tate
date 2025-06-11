package JC_code.javacode;

public class ProjectException extends Exception {
    public ProjectException(String message) {
        super(message);
        printStackTrace();
    }
}