package maexchen.udpHelper;

import java.io.FileInputStream;
import java.io.IOException;
import java.net.URL;
import java.util.Objects;
import java.util.Properties;

public class PropertiesManager {

    private final Properties properties;

    public PropertiesManager() {
        URL resource = Thread.currentThread().getContextClassLoader().getResource("");
        String serverPath = Objects.requireNonNull(resource).getPath() + "server.properties";
        Properties serverProperties = new Properties();
        try {
            serverProperties.load(new FileInputStream(serverPath));
        } catch (IOException e) {
            e.printStackTrace();
        }
        properties = serverProperties;
    }

    public int getServerPort() {
        return Integer.parseInt(properties.getProperty("port"));
    }

    public String getServerHost() {
        return properties.getProperty("ip");
    }
}
