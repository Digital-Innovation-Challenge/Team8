package maexchen.udpHelper;

import java.io.IOException;

public interface MessageSender {

    void send(String message) throws IOException;

}
