package maexchen.simpleBot;

import maexchen.udpHelper.MessageSender;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.io.IOException;

import static org.mockito.Mockito.*;

class SimpleBotTest {

    public static final String BOT_NAME = "myBot";
    public static final String TOKEN = "token";
    public static final String ROLLED = "3,2";
    private MessageSender messageSender = mock(MessageSender.class);
    private SimpleBot simpleBot;

    @BeforeEach
    void setUp() {
        simpleBot = new SimpleBot(BOT_NAME, messageSender);
    }

    @Test
    void shouldJoin_whenRoundStarting() throws IOException {
        simpleBot.onMessage("ROUND STARTING;" + TOKEN);
        verify(messageSender).send("JOIN;" + TOKEN);
    }

    @Test
    void shouldRoll_whenIsOnTurn() throws IOException {
        simpleBot.onMessage("YOUR TURN;" + TOKEN);
        verify(messageSender).send("ROLL;" + TOKEN);
    }

    @Test
    void shouldAnnounce_rolledDice() throws IOException {
        simpleBot.onMessage("ROLLED;" + ROLLED + ";" + TOKEN);
        verify(messageSender).send("ANNOUNCE;" + ROLLED + ";" + TOKEN);
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "UNREGISTERED",
            "HEARTBEAT",
            "ANNOUNCED;player;2,1",
            "PLAYER LOST;player;LIED_ABOUT_MIA",
            "PLAYER ROLLS;player",
            "PLAYER WANTS TO SEE;player",
            "REJECTED",
            "ROUND CANCELED;ONLY_ONE_PLAYER",
            "ROUND STARTED;1;player1,player2",
            "SCORE;player1:5,player2:10",
            })
    void shouldNotRespondTo(String message) throws IOException {
        simpleBot.onMessage(message);
        verify(messageSender, times(1)).send("REGISTER;" + BOT_NAME);
        verifyNoMoreInteractions(messageSender);
    }
}