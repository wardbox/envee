import bme680
import ST7735
import time
from utils.lcd_helper import draw_text_on_lcd

# Configuration
# bme680
sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# st7735
disp = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_BACK,
    dc=9,
    backlight=18,
    rotation=90,
    spi_speed_hz=10000000,
)

disp_width = disp.width
disp_height = disp.height


def main():
    try:
        while True:
            if sensor.get_sensor_data():
                sensor_data = []
                sensor_data.append(
                    f"temp\n{(sensor.data.temperature * (9/5) + 32):.2f} 󰔅"
                )
                sensor_data.append(f"{sensor.data.pressure:.2f}hPa 󰓅")
                sensor_data.append(f"{sensor.data.humidity:.2f}%")

                if sensor.data.heat_stable:
                    sensor_data.append(f"{sensor.data.gas_resistance / 1000}kΩ")

                for i in sensor_data:
                    lcd_ready_image = draw_text_on_lcd(
                        text=i,
                        font_path="./assets/FiraCodeNerdFont-Regular.ttf",
                        font_size=20,
                        text_color=(255, 87, 51, 255),
                        lcd_height=disp_height,
                        lcd_width=disp_width,
                    )

                    disp.display(lcd_ready_image)
                    time.sleep(3)
    except KeyboardInterrupt:
        print("Exiting...")
        disp.set_backlight(0)
        exit()


if __name__ == "__main__":
    main()
