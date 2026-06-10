package com.example.sotuken_ver1

import android.app.Service
import android.content.Context
import android.content.Intent
import android.hardware.usb.UsbManager
import android.os.IBinder
import android.util.Log
import android.widget.Toast
import com.hoho.android.usbserial.driver.UsbSerialPort
import com.hoho.android.usbserial.driver.UsbSerialProber
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch

class TestService :Service() {
    private lateinit var socketClient : SocketClient

    override fun onBind(intent: Intent): IBinder? {
        return null
    }

    override fun onCreate() {
        super.onCreate()
        Log.d("onCreate", "onCreate")
    }

    @OptIn(DelicateCoroutinesApi::class)
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {

        val ipaddr =intent?.getStringExtra("KEY_1")
        val portaddr =intent?.getStringExtra("KEY_2")
        socketClient = SocketClient(ipaddr.toString(), portaddr.toString().toInt())
        Log.d("onStartCommand", "onStartCommand")

        GlobalScope.launch(Dispatchers.Main) {
            val response = socketClient.Connect()
            onResponseReceived(response)
            try {
                while (true){
                    val response2 = socketClient.socketread()
                    socketClient.socketwrite(USBinput(response2))
                }
            }catch (e: Exception){}
        }



        return START_NOT_STICKY
    }

    fun USBconectting():String{
        val response = ByteArray(8192)
        val READ_WAIT_MILLIS=1
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

    fun USBinput(inputcode:String):String{
        val response = ByteArray(8192)
        val READ_WAIT_MILLIS=1
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

        val data2: ByteArray = inputcode.toByteArray()
        port.write(data2,READ_WAIT_MILLIS)

        val len = port.read(response, READ_WAIT_MILLIS);
        val data = response.copyOf(len);
        val serialcode = data.toString(Charsets.UTF_8);


        port.close();

        return serialcode
    }

    fun onResponseReceived(response: String) {
        Toast.makeText(this, response, Toast.LENGTH_LONG).show()

    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("onDestroy", "onDestroy")
    }

    override fun onTaskRemoved(rootIntent: Intent?) {
        super.onTaskRemoved(rootIntent)
        Log.d("onTaskRemoved", "onTaskRemoved")
    }

}