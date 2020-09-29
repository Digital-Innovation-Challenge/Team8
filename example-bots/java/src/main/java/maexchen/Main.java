package maexchen;

import maexchen.simpleBot.SimpleBot;
import maexchen.udpHelper.MessageListener;
import maexchen.udpHelper.PropertiesManager;
import maexchen.udpHelper.UdpCommunicator;

import java.io.IOException;
import java.nio.channels.DatagramChannel;
import java.util.Random;

public class Main {

    public static void main(String[] args) throws IOException {

        UdpCommunicator communicator = new UdpCommunicator(new PropertiesManager(), DatagramChannel.open());
        MessageListener bot = new SimpleBot(getRandomBotName(), communicator.getMessageSender());
        addShutdownHook(communicator);
        communicator.addMessageListener(bot);
        communicator.listenForMessages();
    }

    private static void addShutdownHook(final UdpCommunicator communicator) {
        Runtime.getRuntime().addShutdownHook(new Thread(communicator::stop));
    }

    private static String getRandomBotName() {
        Random random = new Random(System.currentTimeMillis());
        int randomDigits = 10000 + random.nextInt(20000);
        return "example-bot-" + randomDigits;
    }

}
