# password_generater
1. Introduction
Passwords remain the first line of defence for almost every digital account, yet people often choose
weak, memorable passwords because generating and remembering a strong, random one feels
tedious. Ghibli Garden is a desktop application, written entirely in Python using the built-in Tkinter
toolkit, that turns the otherwise dry task of password generation into a small, illustrated ritual. The
interface is painted in the soft, hand-drawn style associated with Studio Ghibli films — watercolour
skies, rolling meadow hills, drifting clouds, and a storybook-style card that hosts the actual controls —
while the underlying logic uses Python's cryptographically secure secrets module to produce genuinely
unpredictable passwords.
This report documents the complete source file, ghibli_password_generator.py, explaining what each
part of the program does, in the order it appears in the file. It is intended as both a project report and a
maintenance reference: a reader with basic Python knowledge should be able to follow the report and
understand exactly how every visual element and every security decision in the program was
implemented.
2. Objectives
• Generate strong, random passwords using a cryptographically secure random number source.
• Give the user fine-grained control over password composition — length, character sets, and
exclusion of visually ambiguous characters.
• Present the tool through a distinctive, hand-crafted graphical interface rather than a generic form.
• Provide immediate, understandable feedback on password strength.
• Keep the entire application self-contained in the Python standard library, requiring no installation
steps.
3. Tools and Technologies Used
Tkinter (including the Canvas, Frame, Entry, Scale, and Checkbutton widgets)
Georgia (headings/labels), Courier New (password display)
Language Python 3
GUI toolkit Randomness / security secrets module (CSPRNG) for all password characters
Character sets string module (ascii_uppercase, ascii_lowercase, digits)
Math utilities math module (log2 for entropy, sin for hill-curve drawing)
Fonts 4. Program Structure Overview
The file is organised into one module-level configuration section and three classes:
• Module level — imports and a shared palette/font configuration used throughout the UI.
• GhibliPasswordGenerator(tk.Tk) — the main application window. It builds the background
scenery, the foreground control panel, and holds all password-generation logic.
• RoundedCard(tk.Frame) — a reusable helper widget that draws a soft rounded-rectangle card,
used as the storybook-style panel background.
• LeafButton(tk.Canvas) — a reusable helper widget that draws a pill-shaped, hand-drawn-feeling
button with hover and click colour changes.
Section 5 below walks through the file from the first line to the last, in the same order the code is written,
explaining every statement.
