package maexchen.udpHelper;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.channels.DatagramChannel;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collection;

public class UdpCommunicator {

    private static final int ONE_SECOND = 1000;
    private static final Charset UTF8 = StandardCharsets.UTF_8;

    private final String remoteHost;
    private final int remotePort;

    private final Collection<MessageListener> listeners = new ArrayList<>();
    private final DatagramChannel channel;

    private volatile boolean shouldStop = false;

    /**
     * Constructs a UdpCommunicator and sets it up to communicate with a remote server.
     */
    public UdpCommunicator() throws IOException {
        PropertiesManager propertiesManager = new PropertiesManager();
        this.remoteHost = propertiesManager.getServerHost();
        this.remotePort = propertiesManager.getServerPort();
        channel = DatagramChannel.open();
        channel.socket().bind(null);
        channel.configureBlocking(false);
    }

    public MessageSender getMessageSender() {
        return message -> {
            InetSocketAddress destination = new InetSocketAddress(remoteHost, remotePort);
            channel.send(UTF8.encode(message), destination);
        };
    }

    /**
     * Makes this UdpCommunicator listen for incoming messages.
     *
     * <p>This will <b>not</b> return, but it will notify all
     * registered {@link MessageListener}s on every incoming message
     * (see {@link UdpCommunicator#addMessageListener(MessageListener)}).</p>
     *
     * <p>
     * The notifications will happen on the same thread which listens for data.
     * Therefore, don't do any lengthy calculations on that thread,
     * as you won't receive further message notifications in the mean time!
     * </p>
     */
    public void listenForMessages() throws IOException {
        Selector selector = Selector.open();
        SelectionKey selectionKey = channel.register(selector, SelectionKey.OP_READ);

        while (!shouldStop) {

            if (selector.select(ONE_SECOND) > 0) {
                selector.selectedKeys().remove(selectionKey);
                if (selectionKey.isReadable()) {
                    readIncomingMessage();
                }
            }
        }

    }

    public void stop() {
        shouldStop = true;

        for (MessageListener listener : listeners) {
            listener.onStop();
        }
    }

    public void addMessageListener(MessageListener listener) {
        listeners.add(listener);
    }

    private void readIncomingMessage() throws IOException {
        String message = readMessageFromChannel();
        for (MessageListener listener : listeners) {
            listener.onMessage(message);
        }
    }

    private String readMessageFromChannel() throws IOException {
        ByteBuffer bytes = ByteBuffer.allocateDirect(1000);
        channel.receive(bytes);
        bytes.flip();
        CharBuffer decoded = UTF8.decode(bytes);
        return decoded.toString();
    }

}