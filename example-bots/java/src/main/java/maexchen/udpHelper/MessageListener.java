package maexchen.udpHelper;

public interface MessageListener {

    void onMessage(String message);

    default void onStop() {
    }

}
