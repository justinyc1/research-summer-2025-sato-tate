package JC_code.src;

public class CustomException extends Exception {
    public CustomException(String message) {
        super(message);
        printStackTrace();
    }
}