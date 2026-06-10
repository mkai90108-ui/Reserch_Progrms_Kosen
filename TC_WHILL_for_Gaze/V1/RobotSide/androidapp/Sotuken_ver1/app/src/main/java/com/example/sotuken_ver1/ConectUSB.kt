package com.example.sotuken_ver1

import android.annotation.SuppressLint
import android.content.Context
import android.hardware.usb.*
import com.hoho.android.usbserial.driver.*
import java.nio.ByteBuffer

class ConectUSB (private val serialPort: Any){
    private val serialPortR: Class<*> = Class.forName("android.hardware.SerialPort")

    fun read(buffer: ByteBuffer): Int {
        val read = serialPortR.getMethod("read", ByteBuffer::class.java)
        return read.invoke(this, buffer) as Int
    }

    fun write(buffer: ByteBuffer, len: Int) {
        val write = serialPortR.getMethod("write", ByteBuffer::class.java, Int::class.java)
        write.invoke(this, buffer, len)
    }

    fun close() {
        val close = serialPortR.getMethod("close")
        close.invoke(this)
    }
}

class SerialManager private constructor(private val serialService: Any) {
    private val serialManager: Class<*> = Class.forName("android.hardware.SerialManager")

    fun openSerialPort(port: String, baudRate: Int): ConectUSB = reflectSerialPort(port, baudRate)

    private fun reflectSerialPort(port: String, baudRate: Int): ConectUSB {
        serialManager.cast(this)
        val openSerialPort = serialManager.getMethod("openSerialPort", String::class.java, Int::class.java)
        return ConectUSB(openSerialPort.invoke(serialManager, port, baudRate))
    }

    companion object {
        fun get(c: Context): SerialManager {
            val serialService = getSerialService(c)
            return SerialManager(serialService)
        }

        @SuppressLint("WrongConstant")
        private fun getSerialService(c: Context) = c.getSystemService("serial") ?: throw Exception("No Serial Service")
    }
}