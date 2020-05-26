from m_video_oop import mvideo_parser as m_p
from m_video_oop import ToDb

if __name__ == '__main__':
    m = m_p()

    while m.button_text != 'next-btn sel-hits-button-next disabled':
        m.mover()

    m.parser()

    ToDb(m.data).to_mongo()





