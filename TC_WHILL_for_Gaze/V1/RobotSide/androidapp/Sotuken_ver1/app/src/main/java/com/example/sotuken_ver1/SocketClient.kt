package com.example.sotuken_ver1

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.DataOutputStream
import java.io.IOException
import java.net.Socket

class SocketClient(private val serverAddress: String, private val portnam: Int) {

    private lateinit var socket: Socket
    suspend fun Connect() : String{
        return withContext(Dispatchers.IO) {
            try {
                socket = Socket(serverAddress, portnam) // PythonサーバーのIPアドレスとポート番号
                val outputStream = DataOutputStream(socket.getOutputStream())
                outputStream.writeUTF("conect")
                outputStream.flush()

                val inputStream = socket.getInputStream()
                val buffer = ByteArray(1024)
                val bytesRead = inputStream.read(buffer)
                val response = String(buffer, 0, bytesRead)
                response
            } catch (e: IOException) {
                e.printStackTrace()
                "エラー: ${e.message}"
            }
        }
    }
    suspend fun socketread() : String{
        val inputStream = withContext(Dispatchers.IO) {
            socket.getInputStream()
        }
        val buffer = ByteArray(1024)
        val bytesRead = withContext(Dispatchers.IO) {
            inputStream.read(buffer)
        }
        val response = String(buffer, 0, bytesRead)

        return response
    }

    suspend fun socketwrite(Outputcode:String){
        val outputStream = DataOutputStream(withContext(Dispatchers.IO) {
            socket.getOutputStream()
        })
        withContext(Dispatchers.IO) {
            outputStream.writeUTF(Outputcode)
        }
        withContext(Dispatchers.IO) {
            outputStream.flush()
        }

    }

    suspend fun close()= withContext(Dispatchers.IO){
        socket.close()

    }

}

