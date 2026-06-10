package com.example.sotuken_ver1

import android.content.Context
import android.content.Intent
import android.hardware.usb.UsbManager
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.hoho.android.usbserial.driver.UsbSerialPort
import com.hoho.android.usbserial.driver.UsbSerialProber
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch


class MainActivity : AppCompatActivity() {
    private lateinit var Button: Button
    private lateinit var Button2: Button
    private lateinit var socketClient : SocketClient


    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        var packageName = "jp.whill.modelc2"
        val intent1 = packageManager.getLaunchIntentForPackage(packageName)

        val intent2 = Intent(this, TestService::class.java)

        var ipinput: EditText = findViewById(R.id.ipinput)
        var portinput: EditText = findViewById(R.id.portinput)

        Button = findViewById(R.id.button)
        Button2 = findViewById(R.id.button2)
        //SocketClient.connect(ipinput.text.toString(), portinput.text.toString().toInt())
        Button.setOnClickListener {
            // エディットテキストのテキストを取得a
            Toast.makeText(
                this,
                ipinput.text.toString() + "\n" + portinput.text.toString(),
                Toast.LENGTH_LONG
            ).show()

            socketClient = SocketClient(ipinput.text.toString(), portinput.text.toString().toInt())
            intent2.putExtra("KEY_1",ipinput.text.toString())
            intent2.putExtra("KEY_2",portinput.text.toString())
            startService(intent2)

            if (intent1 != null){
                startActivity(intent1)
            }else{
                onResponseReceived("app error")
            }
        }

        Button2.setOnClickListener {
            //val response = USBconectting()
            //onResponseReceived(response)
            stopService(intent)
            GlobalScope.launch(Dispatchers.Main) {
                socketClient.close()
            }
            //stopService(intent)
        }
    }

    private fun onResponseReceived(response: String) {
        runOnUiThread {
            // 応答をUIに表示
            Toast.makeText(application, response, Toast.LENGTH_LONG).show()
        }
    }

    private fun USBconectting():String{
        val response = ByteArray(8192)
        val READ_WAIT_MILLIS=10000
        val manager = getSystemService(Context.USB_SERVICE) as UsbManager
        val availableDrivers = UsbSerialProber.getDefaultProber().findAllDrivers(manager)
        if (availableDrivers.isEmpty()) {
            return "エラー"
        }
        val driver = availableDrivers[0]
        val connection = manager.openDevice(driver.device)

        if (connection == null) {
            // ここでUsbManager.requestPermission(driver.device, ..) の処理を追加する
            return "エラー"
        }

        val port = driver.ports[0] // ほとんどのデバイスはポート0しか持っていない
        port.open(connection)
        port.setDTR(true);
        port.setParameters(19200, 8, UsbSerialPort.STOPBITS_1, UsbSerialPort.PARITY_NONE)
        
        val len = port.read(response, READ_WAIT_MILLIS);
        val data = response.copyOf(len);
        val serialcode = data.toString(Charsets.UTF_8);

        port.close();

        return serialcode
    }


}
