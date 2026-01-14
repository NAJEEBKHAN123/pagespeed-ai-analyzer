if __name__ == "__main__":
    if not os.path.exists('.env'):
        st.error("❌ **Configuration Required!** Please create `.env` file with your API key.")
    else:
        main()