import Views.ListScreen
import atexit

main_screen = Views.ListScreen.MainScreen()
main_screen.root.mainloop()
atexit.register(main_screen.before_closure())
