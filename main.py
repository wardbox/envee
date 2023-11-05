import bme680
import ST7735
import time
from PIL import Image, ImageDraw, ImageFont
from lcd_helper import draw_text_on_lcd

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

disp.begin()

width = disp.width
height = disp.height


def main():
    while True:
        if sensor.get_sensor_data():
            output = f"{(sensor.data.temperature * (9/5) + 32):.2f}F, {sensor.data.pressure:.2f}hPa, {sensor.data.humidity:.2f}%"

            if sensor.data.heat_stable:
                print(f"{output}, {sensor.data.gas_resistance}Ohms")
                lcd_ready_image = draw_text_on_lcd(
                    f"{sensor.data.temperature}",
                    "./assets/BebasNeue-Regular.ttf",
                    20,  # font size
                    lcd_height=height,
                    lcd_width=width,
                )
                try:
                    disp.display(lcd_ready_image)
                except:
                    print("Exiting...")
                    disp.set_backlight(0)
                    exit()
            else:
                print(output)
        time.sleep(5)


if __name__ == "__main__":
    main()
