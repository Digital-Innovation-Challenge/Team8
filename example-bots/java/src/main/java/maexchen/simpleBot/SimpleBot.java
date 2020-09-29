package maexchen.simpleBot;

import maexchen.udpHelper.MessageListener;
import maexchen.udpHelper.MessageSender;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Optional;

import static java.util.Optional.of;

public class SimpleBot implements MessageListener {
    public static final String WRONG_NUMBER_OF_PARTS = "Wrong number of message parts: expected %s but got %s";
    public static final String MESSAGE_PART_SEPARATOR = ";";
    protected final MessageSender messageSender;
    protected final String name;

    public SimpleBot(String name, MessageSender messageSender) {
        this.messageSender = messageSender;
        this.name = name;
        String messageString = "REGISTER".concat(MESSAGE_PART_SEPARATOR).concat(name);
        tryToSendMessage(messageString);
    }

    public static void checkContentPartCount(List<String> content, int allowedLength) {
        int contentSize = content.size();
        if (contentSize != allowedLength) {
            String errorMessage = String.format(WRONG_NUMBER_OF_PARTS, allowedLength, contentSize);
            throw new IllegalArgumentException(errorMessage);
        }
    }

    public void onMessage(String message) {
        String securityToken;
        Optional<String> response = Optional.empty();
        System.out.println("SERVER->CLIENT: " + message);
        String[] messageParts = message.split(MESSAGE_PART_SEPARATOR);
        List<String> messageContent = Arrays.stream(messageParts).skip(1).collect(Collectors.toList());
        switch (messageParts[0]) {
            case "ROUND STARTING":
                checkContentPartCount(messageContent, 1);
                securityToken = messageContent.get(0);
                response = of("JOIN".concat(MESSAGE_PART_SEPARATOR).concat(securityToken));
                break;
            case "ROLLED":
                checkContentPartCount(messageContent, 2);
                String diceRoll = messageContent.get(0);
                securityToken = messageContent.get(1);
                response = of("ANNOUNCE"
                        .concat(MESSAGE_PART_SEPARATOR)
                        .concat(diceRoll)
                        .concat(MESSAGE_PART_SEPARATOR)
                        .concat(securityToken));
                break;
            case "YOUR TURN":
                checkContentPartCount(messageContent, 1);
                securityToken = messageContent.get(0);
                response = of("ROLL".concat(MESSAGE_PART_SEPARATOR).concat(securityToken));
                break;
        }
        response.ifPresent(this::tryToSendMessage);
    }

    private void tryToSendMessage(String messageString) {
        try {
            System.out.println("CLIENT->SERVER: " + messageString);
            messageSender.send(messageString);
        } catch (IOException e) {
            System.err.println("Failed to send " + messageString + ": " + e.getMessage());
        }
    }

    public void onStop() {
        tryToSendMessage("UNREGISTER");
    }
}
